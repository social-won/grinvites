"""Persistent mail daemon — checks every 60 s and sends iCal invites to users
whose invite_times schedule matches the current day and time (±5 min window)."""

import asyncio
import logging
import os
import sys
import uuid
from typing import Any
from datetime import datetime, timedelta, timezone
from icalendar import Event, ROLE
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "api"))

from api.db_functions import get_events_within_two_weeks, get_users_for_event_full, if_user_emailed_for_event, get_event_by_id
from api.mail.config import config, Config
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
_SENDER_ADDRESS = MailAddress.new(
    Config.grinvites_mail_address, cn="Grinvites", role=ROLE.CHAIR
)


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
    """Return event duration; fall back to 1 hour when end_time is missing.

    Args:
        start_str (str): _description_
        end_str (str | None): _description_

    Returns:
        timedelta: _description_
    """

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


def _build_attendees(users) -> list[vCalAddress]:
    attendees = []
    for user in users:
        try:
            addr = vCalAddress.new(
                user.email,
                cn=user.display_name,
                language="English"
            )
            attendees.append(addr)
        except Exception as exc:
            log.warning("Skipping %s — invalid address: %s", user.email, exc)
    return attendees

def _build_request_event(event_id: str, attendees: list[vCalAddress]) -> Event:
    event : dict[str, Any] = get_event_by_id(event_id=event_id)
    return RequestEvent.grinvites_event(
        uid=uuid.UUID(int = int(event_id)),
        stamp=event["creation_time_stamp"],
        summary=event["title"],
        description=event["summary"],
        start=event["start_time"],
        duration=datetime.fromisoformat(event["end_time"])-datetime.fromisoformat(event["start_time"]),
        location=event["location"] if event["location"] != '' else Config.grinnell_college_address,
        organizer=vCalAddress(f'mailto:{Config.grinvites_mail_address}'),
        status=STATUS.CONFIRMED,
        priority=0,
        attendees=attendees,
        classification=CLASS.PUBLIC,
        transparency=TRANSP.OPAQUE,
        sequence=0,
    )

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

    request_event = _build_request_event(event["id"], attendees)

    prod_id = ProdID(*Config.grinvites_prod_id, is_nonSGML=True)

    ics = ICSFile(request_event, prod_id, method=METHOD.REQUEST)
    msg = ics.to_MIME()

    addresses = ", ".join(a.email for a in attendees)
    log.info(
        "Sending invite for event %s (%s) via %s:%d → %s",
        event["id"], event["title"], server.hostname, server.port, addresses,
    )
    try:
        server.send_message(
            msg,
            recipient_addresses=attendees,
            sender_address=_SENDER_ADDRESS,
            user=config.smtp_login,
            password=config.api_key,
        )

        # NEED A WAY TO INDICATE USER HAS BEEN SENT EVENT
        # for attendee in (attendee.email for attendee in attendees):
        #     update_user_been_sent_event(attendee, event["id"])

        log.info("Sent invite for event %s (%s) to %d recipient(s).", event["id"], event["title"], len(attendees))
    except Exception as exc:
        log.error("Failed to send invite for event %s: %s", event["id"], exc)


def _dispatch_cycle(config: Config, server: MailServer) -> None:
    """A single mail disbatch run. Sweeps database for all events within two weeks and mails out all matching recipients

    Args:
        config (Config): _description_
        server (MailServer): _description_
    """
    log.info("Checking events within the next two weeks.")
    events = get_events_within_two_weeks()
    log.info("Found %d upcoming event(s).", len(events))
    if not events:
        return

    matches = 0
    for event in events:
        users = [user for user in get_users_for_event_full(event["id"]) if not if_user_emailed_for_event(user, event["id"]) ]
        if not users:
            continue # no users matched to event
        unsent_users = users
        matched = len(unsent_users)
        matches += matched
        _send_event_invite(event, unsent_users, config, server)


    log.info("Dispatch cycle complete — %d user(s) matched the current window.", matches)


async def run_daemon() -> None:
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
