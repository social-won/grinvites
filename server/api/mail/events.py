from icalendar import Event, CLASS, STATUS, TRANSP, vRecur, vCalAddress
from server.api.mail.mail_exchange import MailAddress
from icalendar.error import InvalidCalendar
from datetime import date, datetime, timedelta, timezone
from typing import Sequence
from lorem_text import lorem
from .config import Config
import uuid


class RequestEvent(Event):
    """A vEvent calendar component consisting of a grouping of event properties defined by the RFC

    Args:
        Event (Event): A grouping of component properties that describe an event.
    """

    @classmethod
    def grinvites_event(
        cls,
        uid: str | uuid.UUID,
        summary: str,
        description: str,
        start: date | datetime,
        duration: timedelta,
        location: str,
        organizer: vCalAddress,
        status: STATUS,
        priority: int,
        stamp: date,
        attendees: list[vCalAddress],
        classification: CLASS = CLASS.PUBLIC,
        categories: Sequence[str] = (),
        recurrence: (
            list[tuple[date, None] | tuple[datetime, None] | tuple[datetime, datetime]]
            | list[vRecur]
            | None
        ) = None,
        last_modified: date | None = None,
        comments: list[str] | str | None = None,
        created: date | None = None,
        sequence: int | None = None,
        transparency: TRANSP = TRANSP.OPAQUE,
    ) -> Event:
        event = super(RequestEvent, cls).new(
            uid=uid,
            stamp=stamp,
            summary=summary,
            description=description,
            location=location,
            organizer=organizer,
            categories=categories,
            status=status,
            priority=priority,
            last_modified=last_modified,
            comments=comments,
            attendees=attendees,
            classification=classification,
            created=created,
            sequence=sequence,
            transparency=transparency,
        )

        event.set_start(start=start)
        event.set_duration(duration=duration)

        # RDATE: Type checking for list[tuple(a, b)]
        if recurrence is not None:
            if isinstance(recurrence, list) and all(
                isinstance(x, tuple) and len(x) == 2 for x in recurrence
            ):

                #  Type checking for either list[tuple[datetime, None]], list[tuple[date, None]], or list[tuple[datetime, datetime]]
                if (
                    all(isinstance(x[0], date) and x[1] == None for x in recurrence)
                    or all(
                        isinstance(x[0], datetime) and x[1] == None for x in recurrence
                    )
                    or all(
                        isinstance(x[0], datetime) and isinstance(x[1], datetime)
                        for x in recurrence
                    )
                ):
                    event.add("RDATE", recurrence)
                else:
                    raise InvalidCalendar(f"The provided RDATE is invalid.")

            #  RRULE: Type checking for list[vRecur]
            elif isinstance(recurrence, list) and all(
                isinstance(x, vRecur) for x in recurrence
            ):
                event.add("RRULE", recurrence)
            else:
                raise InvalidCalendar(f"The provided RRULE is invalid.")

        return event

    @classmethod
    def request_example(
        cls,
        name: str = "rfc_9074_example_3",
        attendees: list[vCalAddress] | None = None,
    ):

        event = super().example(name=name)

        if attendees:
            event.attendees = attendees
        return event

    @staticmethod
    def test1_grinvites_event(attendees: list[vCalAddress]):

        return RequestEvent.grinvites_event(
            uid=uuid.uuid4(),
            stamp=datetime.now(timezone.utc),
            summary=f'Grinvites Test Test Event {datetime.now(timezone.utc).strftime("%B %d, %Y %H:%M:%S")}',
            description=lorem.sentence(),
            start=datetime.now(timezone.utc),
            duration=timedelta(hours=1),
            location=Config.grinnell_college_address,
            organizer=vCalAddress(Config.grinvites_mail_address),
            status=STATUS.CONFIRMED,
            priority=0,
            attendees=attendees,
            classification=CLASS.PUBLIC,
            sequence=0,
            transparency=TRANSP.OPAQUE,
        )
