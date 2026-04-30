import smtplib
import socket
from domain_validator import DomainValidator
from ipaddress import ip_address
from datetime import datetime, timezone, timedelta
from icalendar import Calendar, Event, vCalAddress, CUTYPE, ROLE, PARTSTAT
from icalendar.parser import Parameters
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email_validator import validate_email as validate_email
from icalendar.prop.cal_address import vCalAddress
from icalendar.enums import CUTYPE, ROLE, PARTSTAT
from iso639 import Lang
from utils import get_enum_value, get_iso639_language_name
from error import (
    InvalidCalendarAddress,
    UndeliverableMailAddress,
    invalid_parameter_error_message,
)
from typing import Any
import dns.resolver
import re

class MailServer:

    def __init__(self, hostname: str, port: int) -> None:
        """MailServer Constructor

        Args:
            server (str): smtp server hostname.
            port (int): The preferred outbound mail traffic port. MailServer will attempt the preferred port. If the provided port is unreachable MailServer will default to one of the default secure SMTP ports.
            Default ports = [587, 465, 2525]
        """

        if not self._is_resolvable_host(hostname):
            raise ValueError("Hostname is not resolvable.")
        self.hostname = hostname

        if MailServer._is_smtp_server_live(hostname, port, timeout=5):
            self.port = port
        else:
            for port in [587, 465, 2525]:
                if MailServer._is_smtp_server_live(hostname, port, timeout=5):
                    self.port = port
                    break
            if not self.port:
                raise ValueError("Provided host has no reachable secure outbound port")

    @staticmethod
    def _is__mail_port(port: int) -> bool:
        """Checks if the provided port is a secure mail port.

        Args:
            ports (int): server endpoint
            Range 0-65535
        Returns:
            bool: wether the provided port is accessible
        """
        return port in [587, 2525, 465]

    @staticmethod
    def _is_resolvable_host(hostname: str) -> bool:
        """Checks wether the provided host name is resolvable

        Args:
            host (str): Hostname

        Returns:
            bool: wether the provided hostname is resolvable
        """
        try:
            MailServer._is_resolvable_domain(
                MailServer._get_hostname_ip_address(hostname)
            )
            return True
        except:
            return False

    @staticmethod
    def _is_resolvable_domain(domain: str) -> bool:
        """Boolean indicating if the provided domain posses an active mail exchange.

        Args:
            domain (str): complete domain name.

        Returns:
            bool: wether the provided domain is valid
        """
        try:
            dns.resolver.resolve(domain, "MX")
            return True
        except:
            return False

    @staticmethod
    def _is_valid_V4_V6_address(address: str) -> bool:
        try:
            ip_address(address)
            return True
        except:
            return False

    @staticmethod
    def _is_smtp_server_live(host: str, port: int, timeout: int = 5) -> bool:

        if not MailServer._is__mail_port(port):
            return False
        try:
            if port == 465:
                smtp = smtplib.SMTP_SSL(host, port, timeout=timeout)
            else:
                smtp = smtplib.SMTP(host, port, timeout=timeout)
                smtp.starttls()

            with smtp:
                response_code, _ = smtp.noop()
                return 200 <= response_code < 300
        except:
            return False

    @staticmethod
    def _get_hostname_ip_address(hostname: str) -> str:
        return socket.gethostbyname(hostname)

    def send_message(
        self,
        msg: MIMEMultipart | MIMEText | MIMEBase,
        recipient_address: MailAddress,
        sender_address: MailAddress,
        user: str,
        password: str,
    ) -> None:

        try:
            if self.port == 465:
                smtp = smtplib.SMTP_SSL(self.hostname, self.port)
            else:
                smtp = smtplib.SMTP(self.hostname, self.port)
                smtp.starttls()
            with smtp:
                smtp.login(user, password)
                smtp.sendmail(
                    sender_address.email, recipient_address.email, msg.as_string()
                )

        except smtplib.SMTPHeloError:
            print(
                "DELIVERY FAILURE: The server didn't reply properly to the helo greeting."
            )
        except smtplib.SMTPAuthenticationError:
            print(
                "DELIVERY FAILURE: The server didn't accept the username/password combination."
            )
        except smtplib.SMTPNotSupportedError:
            print("DELIVERY FAILURE: The AUTH command is not supported by the server.")
        except smtplib.SMTPRecipientsRefused:
            print(
                "DELIVERY FAILURE: The server rejected ALL recipients (no mail was sent)."
            )
        except smtplib.SMTPSenderRefused:
            print(f"DELIVERY FAILURE: The server didn't accept the sender_address. {sender_address.email}")
        except smtplib.SMTPDataError as e:
            print(
                f"DELIVERY FAILURE: The server replied with an unexpected error code (other than a refusal of a recipient).\nEROOR: {e.smtp_code}. {e.smtp_error}"
            )
        except Exception as e:
            print(f"DELIVERY FAILURE: {e}")


class MailAddress(vCalAddress):
    """A subclass of vCalAddress.

    Args:
        vCalAddress (vCalAddress): _description_
    """

    def __new__(
        cls,
        string_address: str,
        /,
        common_name: str | None = None,
        cutype: str | CUTYPE | None = None,
        delegated_from: str | MailAddress | vCalAddress | None = None,
        delegated_to: str | MailAddress | vCalAddress | None = None,
        directory: str | None = None,
        language: str | Lang | None = None,
        partstat: str | PARTSTAT | None = None,
        role: str | ROLE | None = None,
        rsvp: bool | None = None,
        sent_by: str | MailAddress | vCalAddress | None = None,
    ) -> str:

        params : dict[str, Any] = {}
        if not cls._is_valid_local_part_and_domain(string_address):
            raise InvalidCalendarAddress(
                f"The provided string address: {string_address} is not valid."
            )

        if not cls._is_deliverable_mail_address(vCalAddress(string_address).email):
            raise UndeliverableMailAddress(
                f"The provided string address: {string_address} is undeliverable."
            )

        if common_name:
            params["CN"] = common_name

        if cutype is not None:
            try:
                params["CUTYPE"] = get_enum_value(CUTYPE, cutype)
            except:
                print(invalid_parameter_error_message(CUTYPE, "cutype"))

        if delegated_from is not None:
            try:
                params["DELEGATED-FROM"] = vCalAddress._get_email(delegated_from)
            except:
                print(invalid_parameter_error_message(MailAddress, "delegated_from"))
                print(invalid_parameter_error_message(vCalAddress, "delegated_from"))

        if delegated_to is not None:
            try:
                params["DELEGATED-TO"] = vCalAddress._get_email(delegated_to)
            except:
                print(invalid_parameter_error_message(MailAddress, "delegated_to"))
                print(invalid_parameter_error_message(vCalAddress, "delegated_to"))

        if directory is not None:
            params["DIRECTORY"] = directory

        if language is not None:
            try:
                params["LANGUAGE"] = get_iso639_language_name(language)
            except:
                print(invalid_parameter_error_message(Lang, "language"))

        if partstat is not None:
            try:
                params["PARTSTAT"] = get_enum_value(PARTSTAT, partstat)
            except:
                print(invalid_parameter_error_message(PARTSTAT, "partstat"))

        if role is not None:
            try:
                params["ROLE"] = get_enum_value(ROLE, role)
            except:
                print(invalid_parameter_error_message(ROLE, "role"))

        if rsvp is not None:
            params["RSVP"] = str(rsvp)

        if sent_by is not None:
            try:
                params["SENT-BY"] = vCalAddress._get_email(sent_by)
            except:
                print(invalid_parameter_error_message(MailAddress, "sent_by"))
                print(invalid_parameter_error_message(vCalAddress, "sent_by"))

        return super().__new__(cls, vCalAddress._get_email(string_address), "utf-8", params=params)

    @classmethod
    def individual_request(
        cls,
        string_address: str,
        /,
        common_name: str | None = None,
        delegated_from: MailAddress | vCalAddress | None = None,
        delegated_to: MailAddress | vCalAddress | None = None,
        directory: str | None = None,
        language: str | Lang | None = None,
        rsvp: bool = True,
        sent_by: str | MailAddress | vCalAddress | None = None,
    ):

        return MailAddress(string_address,
                           common_name = common_name,
                           cutype = CUTYPE.INDIVIDUAL,
                           delegated_from = delegated_from,
                           delegated_to = delegated_to,
                           directory =  directory,
                           language = language,
                           partstat = PARTSTAT.NEEDS_ACTION,
                           role = ROLE.OPT_PARTICIPANT,
                           rsvp = rsvp,
                           sent_by = sent_by)

    @staticmethod
    def get_email(email: str | MailAddress | vCalAddress) -> str:
        if isinstance(email, vCalAddress) or isinstance(email, MailAddress):
            return email.email
        else:
            try:
                MailAddress._is_valid_local_part_and_domain(email)
                return vCalAddress(email).email
            except:
                raise InvalidCalendarAddress(f"{email} is not a valid mail address.")

    @classmethod
    def _is_valid_local_part_and_domain(cls, string_address: str) -> bool:
        string_address = vCalAddress(string_address).email
        if string_address.count("@") != 1:
            raise ValueError(
                "Address is missing single '@' between username and domain."
            )
        else:
            local_part = string_address.split("@")[0]
            domain = string_address.split("@")[1]

            if not cls._is_valid_local_part(local_part):
                raise ValueError("Invalid address localpart (username).")
            if not MailServer._is_resolvable_host(domain):
                raise ValueError("Invalid address domain syntax.")
            else:
                return True

    @staticmethod
    def _is_valid_local_part(localPart: str) -> bool:
        """Boolean indicating if the email local part is of valid form.

        Args:
            localPart (str): string proceeding email address '@'

        Returns:
            bool: wether the provided localPart is valid.
        """
        if (
            len(localPart) <= 64
            and len(localPart) >= 1
            and re.match(
                r"^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*$",
                localPart,
            )
        ):
            return True
        else:
            return False

    @staticmethod
    def _is_deliverable_mail_address(string_address: str) -> bool:
        """_summary_

        Args:
            string_address (str): _description_

        Returns:
            bool: _description_
        """
        try:
            validate_email(vCalAddress(string_address).email, check_deliverability=True)
            return True
        except:
            return False

    def to_string(self) -> str:
        """Returns string format of email address.

        Returns:
            str: email address.
        """
        return self.email

    def get_common_name(self) -> str:
        """Returns the common name associated with MailAddress.

        Returns:
            str: common name as string.
        """
        return self.CN if self.CN else ""
