from enum import Enum


class METHOD(Enum):
    """defines the property "METHOD" for the method
    types that are applicable to the "VEVENT" calendar component."""

    PUBLISH = "PUBLISH"
    """Used to publish an iCalendar object to one or
    more Calendar Users.  There is no interactivity
    between the publisher and any other calendar
    user.  An example might include a baseball team
    publishing its schedule to the public."""

    REQUEST = "REQUEST"
    """Used to schedule an iCalendar object with other
    Calendar Users.  Requests are interactive in
    that they require the receiver to respond using
    the reply methods.  Meeting requests, busy time
    requests and the assignment of tasks to other
    Calendar Users are all examples.  Requests are
    also used by the "Organizer" to update the
    status of an iCalendar object."""

    REPLY = "REPLY"
    """A reply is used in response to a request to
    convey "Attendee" status to the "Organizer".
    Replies are commonly used to respond to meeting
    and task requests."""

    ADD = "ADD"
    """Add one or more new instances to an existing
    recurring iCalendar object."""

    CANCEL = "CANCEL"
    """Cancel one or more instances of an existing
    iCalendar object."""

    REFRESH = "REFRESH"
    """The Refresh method is used by an "Attendee" to
    request the latest version of an iCalendar
    object."""

    COUNTER = "COUNTER"
    """The Counter method is used by an "Attendee" to
    negotiate a change in an iCalendar object.
    Examples include the request to change a
    proposed event time or change the due date for a
    task."""

    DECLINECOUNTER = "DECLINECOUNTER"
    """Used by the "Organizer" to decline the proposed
    counter-proposal."""
