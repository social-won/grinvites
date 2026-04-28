from icalendar import Event, STATUS, TRANSP, vCalAddress
from icalendar.cal.component import Component
from datetime import date, datetime, timezone
import uuid

class RequestEvent(Event):
    """A vEvent calendar component consisting of a grouping of event properties defined by the RFC 

    Args:
        Event (Event): A grouping of component properties that describe an event.
    """


    def __init__(self,
                 uid: uuid.UUID,
                 sequence: int,
                 start: date | datetime,
                 end: date | datetime,
                 summary: str,
                 description: str ,
                 location: str,
                 attendees: list[vCalAddress],
                 organizer: vCalAddress,
                 status: STATUS ,
                 transparency: TRANSP
                 ):

        if Component._validate_start_and_end(start, end):
            super().new(uid=uid,
                        sequence=sequence,
                        stamp=datetime.now(timezone.utc),
                        start=start,
                        end=end,
                        summary=summary,
                        description=description,
                        location=location,
                        attendees=attendees,
                        status=status,
                        organizer=organizer,
                        transparency=transparency)

    @classmethod
    def GrinvitesEvent():
        
    @classmethod
    def test_example(cls):
        return cls.new()