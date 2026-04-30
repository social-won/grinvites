from icalendar import Event, CLASS, STATUS, TRANSP, vRecur, vCalAddress
from icalendar.error import InvalidCalendar
from datetime import date, datetime, timedelta
from typing import Sequence
import uuid


class RequestEvent(Event):
    """A vEvent calendar component consisting of a grouping of event properties defined by the RFC

    Args:
        Event (Event): A grouping of component properties that describe an event.
    """

    def __init__(
        self,
        uid: str | uuid.UUID | None = None,
        summary: str | None = None,
        description: str | None = None,
        start: date | datetime | None = None,
        location: str | None = None,
        organizer: vCalAddress | str | None = None,
        categories: Sequence[str] = (),
        status: STATUS | None = None,
        priority: int | None = None,
        last_modified: date | None = None,
        comments: list[str] | str | None = None,
        attendees: list[vCalAddress] | None = None,
        classification: CLASS | None = None,
        stamp: date | None = None,
        created: date | None = None,
        sequence: int | None = None,
        transparency: TRANSP | None = None,
    ):

        return super().new(
            uid=uid,
            summary=summary,
            description=description,
            start=start,
            location=location,
            organizer=organizer,
            categories=categories,
            status=status,
            priority=priority,
            last_modified=last_modified,
            comments=comments,
            attendees=attendees,
            classification=classification,
            stamp=stamp,
            created=created,
            sequence=sequence,
            transparency=transparency,
        )

    @classmethod
    def GrinvitesEvent(
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
        stamp: date | None = None,
        created: date | None = None,
        sequence: int | None = None,
        transparency: TRANSP = TRANSP.OPAQUE,
    ):
        event = RequestEvent(
            uid=uid,
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
            stamp=stamp,
            created=created,
            sequence=sequence,
            transparency=transparency,
        )

        event.set_start(start=start)
        event.set_duration(duration=duration)

        # RDATE: Type checking for list[tuple(a, b)]
        if isinstance(recurrence, list) and all(
            isinstance(x, tuple) and len(x) == 2 for x in recurrence
        ):

            #  Type checking for either list[tuple[datetime, None]], list[tuple[date, None]], or list[tuple[datetime, datetime]]
            if (
                all(isinstance(x[0], date) and x[1] == None for x in recurrence)
                or all(isinstance(x[0], datetime) and x[1] == None for x in recurrence)
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

        event = super().example(name = name)

        if attendees:
            event.attendees = attendees
        return event
