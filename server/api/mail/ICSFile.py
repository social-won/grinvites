from iso639 import Lang, is_language
from iso639.exceptions import InvalidLanguageValue
from datetime import datetime, timezone, timedelta
from icalendar import Calendar, Event, vCalAddress, CUTYPE, ROLE,PARTSTAT
from icalendar.prop.text import vText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from Method import Method
class ICSFile:

    def __init__(self, iCal_event: Event, prod_id: ProdID, method : Method, version: int = 2, calendar_scale: str="GREGORIAN"):

        self.version = vText(f'{version:.1f}')
        self.calendar_scale = vText(calendar_scale)
        self.prod_id = prod_id.to_vText()
        self.method = vText(method.name)

class ProdID:
    def __init__(self, vendor_name:str , product_name: str, language:str, is_nonSGML: bool=True):
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

    def to_string(self):
        return f'-//{self.vendor_name}//{"NONSGML " if self.is_nonSGML else ""}{self.product_name}//{self.language}'

    def to_vText(self):
        return vText(self.to_string())
