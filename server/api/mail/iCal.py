from __future__ import annotations
from iso639 import Lang, is_language
from iso639.exceptions import InvalidLanguageValue
from icalendar import Calendar, Event, vCalAddress
from icalendar.prop.text import vText
from email.mime.text import MIMEText
from email.utils import formataddr
from .enums import METHOD
from .events import RequestEvent
from .utils import get_enum_value
from .config import config

class ICSFile:

    def __init__(
        self,
        ical_event: Event | RequestEvent,
        prod_id: ProdID,
        method: str | METHOD,
        version: int = 2,
        calendar_scale: str = "GREGORIAN",
    ):
        """ICS file constructor.

        Args:
            ical_event (Event | RequestEvent): event object to be made into an ics file.
            prod_id (ProdID): production id signature for vCal event
            method (str | METHOD): VEVENT calendar component method.
            version (int, optional): vCalendar version. Defaults to 2.
            calendar_scale (str, optional): Calendar scale. Defaults to "GREGORIAN".
        """
        self.event = ical_event
        self.method = method
        self.calendar = Calendar()
        self.set_calendar_property("prodid", prod_id)
        self.set_calendar_property("method", get_enum_value(METHOD, method))
        self.set_calendar_property("calscale", calendar_scale)
        self.set_calendar_property("version", f"{version:.1f}")
        self.calendar.add_component(ical_event)

    def to_MIME(self, decoding="utf-8"):
        calendar_message = MIMEText(
            self.calendar.to_ical().decode(decoding), "calendar"
        )
        calendar_message["To"] = ICSFile.format_addresses_for_mime(self.event.attendees)
        calendar_message["From"] = config.grinvites_mail_address_rfc5322
        calendar_message["Subject"] = self.event.summary
        calendar_message.set_param("method", get_enum_value(METHOD, self.method))
        calendar_message.add_header(
            "Content-class", "urn:content-classes:calendarmessage"
        )
        # encoders.encode_base64(calendar_message)
        return calendar_message

    def set_calendar_property(self, name: str, value):
        while name in self.calendar:
            del self.calendar[name]

        self.calendar.add(name, value)

    @staticmethod
    def format_addresses_for_mime(attendees: list[vCalAddress]) -> str:
        """Converts a list of icalendar vCalAddress objects into a single
        RFC 5322 compliant string suitable for MIME 'To' or 'Cc' headers.

            Args:
                attendees (list[vCalAddress]): list of attendees.

            Returns:
                str: string of attendees, RFC 5322 compliant.
        """

        formatted_addresses = []

        for attendee in attendees:
            if isinstance(str(attendee.name), str) and len(attendee.name) >= 1:
                name = attendee.name
            else:
                name = ''

            address = attendee.email
            if address.upper().startswith('MAILTO:'):
                email_address = address[7:]
            else:
                email_address = address

            formatted_addresses.append(formataddr((name, email_address)))

        return ", ".join(formatted_addresses)


class ProdID:
    def __init__(
        self,
        vendor_name: str,
        product_name: str,
        language: str,
        is_nonSGML: bool = True,
    ):
        """Specifies the values of the identifier for the product that created the iCalendar object.

        Example PRODID:
            PRODID:-//ABC Corporation//NONSGML My Product//EN

        Args:
            vendor_name (str): The name of the organization creating the file.
            (e.g., ABC Corporation).

            product_name (str): The application name.
            (e.g., Google Calendar)

            language_code (str): ISO 639 language code.
            (e.g., EN for English).
        """
        language = language.lower().capitalize()

        self.vendor_name = vendor_name
        self.product_name = product_name
        if is_language(language):
            self.language = Lang(language).pt1.upper()
        else:
            raise InvalidLanguageValue
        self.is_nonSGML = is_nonSGML

    def to_string(self) -> str:
        """Transforms ProdID to formatted string

        Returns:
            str: Formatted string of ProdID
        """
        return f'-//{self.vendor_name}//{"NONSGML " if self.is_nonSGML else ""}{self.product_name}//{self.language}'

    def to_vText(self) -> vText:
        """Transforms ProdID to vText of formatted string.

        Returns:
            vText: Formatted vText of ProdID.
        """
        return vText(self.to_string())
