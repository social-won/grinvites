"""Persistent mail daemon — checks every 60 s and sends iCal invites to users
whose invite_times schedule matches the current day and time (±5 min window)."""

import asyncio
import logging
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone

# Make the mail library's local imports resolvable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "api", "mail"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "api"))

from api.db_functions import get_events_within_two_weeks, get_users_for_event_full
from api.mail.config import Config
from api.mail.enums import METHOD
from api.mail.events import RequestEvent
from api.mail.iCal import ICSFile, ProdID
from api.mail.mail_exchange import MailAddress, MailServer
from icalendar import vCalAddress, STATUS, CLASS, TRANSP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [daemon] %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)

_DAY_SHORT = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
_TOLERANCE = timedelta(minutes=5)


def _is_scheduled_now(invite_times: dict[str, str]) -> bool:
    """True if the user's invite_times contains today with a time within ±5 min of now."""
    now = datetime.now()
    day_key = _DAY_SHORT[now.weekday()]
    if day_key not in invite_times:
        return False
    try:
        scheduled = datetime.strptime(invite_times[day_key], "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
    except ValueError:
        return False
    return abs(now - scheduled) <= _TOLERANCE


def _parse_duration(start_str: str, end_str: str | None) -> timedelta:
    """Return event duration; fall back to 1 hour when end_time is missing."""
    if not end_str:
        return timedelta(hours=1)
    fmt = "%Y-%m-%dT%H:%M:%S"
    try:
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str)
        delta = end - start
        return delta if delta.total_seconds() > 0 else timedelta(hours=1)
    except ValueError:
        return timedelta(hours=1)


def _build_attendees(users) -> list[MailAddress]:
    attendees = []
    for user in users:
        try:
            addr = MailAddress.individual_request(
                f"mailto:{user.email}", common_name=user.display_name
            )
            attendees.append(addr)
        except Exception as exc:
            log.warning("Skipping %s — invalid address: %s", user.email, exc)
    return attendees


def _send_event_invite(event: dict, users, config: Config, server: MailServer) -> None:
    attendees = _build_attendees(users)
    if not attendees:
        log.info("Event %s — no valid attendees, skipping.", event["id"])
        return

    start_str = event["start_time"]
    try:
        start = datetime.fromisoformat(start_str).replace(tzinfo=timezone.utc)
    except ValueError:
        log.warning("Event %s — unparseable start_time %s, skipping.", event["id"], start_str)
        return

    duration = _parse_duration(event["start_time"], event.get("end_time"))

    organizer = vCalAddress(config.grinvites_mail_address)
    prod_id = ProdID(*config.grinvites_prod_id, language="English")

    ical_event = RequestEvent.grinvites_event(
        uid=uuid.uuid4(),
        stamp=datetime.now(timezone.utc),
        summary=event["title"],
        description=event.get("description") or "",
        start=start,
        duration=duration,
        location=event.get("location") or config.grinnell_college_address,
        organizer=organizer,
        status=STATUS.CONFIRMED,
        priority=0,
        attendees=attendees,
        classification=CLASS.PUBLIC,
        transparency=TRANSP.OPAQUE,
        sequence=0,
    )

    ics = ICSFile(ical_event, prod_id, method=METHOD.REQUEST)
    msg = ics.to_MIME()

    sender = MailAddress(
        f"mailto:{config.grinvites_mail_address}",
        common_name="Grinvites",
    )

    addresses = ", ".join(a.email for a in attendees)
    log.info(
        "Sending invite for event %s (%s) via %s:%d → %s",
        event["id"], event["title"], server.hostname, server.port, addresses,
    )
    try:
        server.send_message(
            msg,
            recipient_addresses=attendees,
            sender_address=sender,
            user=config.smtp_login,
            password=config.api_key,
        )
        log.info("Sent invite for event %s (%s) to %d recipient(s).", event["id"], event["title"], len(attendees))
    except Exception as exc:
        log.error("Failed to send invite for event %s: %s", event["id"], exc)


def _dispatch_cycle(config: Config, server: MailServer) -> None:
    log.info("Polling — checking events within the next two weeks.")
    events = get_events_within_two_weeks()
    log.info("Found %d upcoming event(s).", len(events))
    if not events:
        return

    matches = 0
    for event in events:
        users = get_users_for_event_full(event["id"])
        if not users:
            continue
        scheduled_users = [u for u in users if _is_scheduled_now(u.invite_times)]
        if not scheduled_users:
            continue
        matches += len(scheduled_users)
        _send_event_invite(event, scheduled_users, config, server)

    log.info("Dispatch cycle complete — %d user(s) matched the current window.", matches)


async def run_daemon() -> None:
    config = Config()
    try:
        server = MailServer(config.bulk_mail_smtp_url, config.default_smtp_port)
    except ValueError as exc:
        log.critical("Cannot reach mail server: %s", exc)
        return

    log.info("Daemon started — polling every 60 s.")
    while True:
        try:
            _dispatch_cycle(config, server)
        except Exception as exc:
            log.error("Dispatch cycle error: %s", exc)
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(run_daemon())
