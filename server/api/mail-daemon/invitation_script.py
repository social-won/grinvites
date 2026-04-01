import smtplib
import random
from datetime import datetime, timezone, timedelta
from icalendar import Calendar, Event, vCalAddress, CUTYPE, ROLE,PARTSTAT
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# producing iCalendar
cal = Calendar()
cal.add('prodid', "-//Grinnell College//NONSGML grinvites//EN")
cal.add('version', "2.0")
cal.add('method', "REQUEST")
cal.add('calscale', 'GREGORIAN')

today_at_time = datetime.now(timezone.utc).replace(
    hour=14,
    minute=30,
    second=0)

sender_email = "hello@grinvites.app"
receiver_email = "sackmann@grinnell.edu"
event_name = "Brazilian Jiu-Jitsu Classs"

organizer = vCalAddress.new(
    "hello@grinvites.com",  # email address
    cn="Grinvites Testing"  # common name
)

# Making VENV
event = Event()
event.add("summary", event_name)
event.add('created', datetime.now(timezone.utc))
event.add('dtstamp', datetime.now(timezone.utc))
event.add('dtstart', today_at_time + timedelta(weeks=1))
event.add('dtend', today_at_time + timedelta(weeks=1, hours=1))
event.add('uid', f'5341-{datetime.now()}-system@grinvites.app')
event.add('sequence' , 0)
event.add('status', 'confirmed')
event.add('organizer', organizer)

# adding ATTENDEE(S)
attendee = vCalAddress.new(
    receiver_email,  # email address
    cn="Grant Sackmann",           # common name
    cutype=CUTYPE.INDIVIDUAL,   # calendar user type
    role=ROLE.OPT_PARTICIPANT,            # role
    partstat=PARTSTAT.NEEDS_ACTION, # participation status
    rsvp=False,                  # RSVP requirement
)

API_KEY = "975f2bd4f6202f6a11ea38e07f3a6e95"
event.attendees = [attendee] # adding attendee to event

cal.add_component(event)
ics_data = cal.to_ical().decode('utf-8')

# producing Multipurpose Internet Mail Extension Sturcutre for client parsiing
msg = MIMEMultipart('mixed') # mixed: for processing inline message bodies and file attachments
msg['Subject'] = event_name
msg['From'] = sender_email
msg['To'] = receiver_email
# Microsoft specific header to force calendar parsing
msg.add_header("Content-class", "urn:content-classes:calendarmessage")

# Alternative texts
text="""Brazilian Jiu-Jitsu class. Each class is self-contained and welcoming to beginners and advanced players. Classes consist of warm-up exercises and drills, learning of specific techniques and live rolling.&nbsp;"""
html="""<picture class="lw_image">  <source type="image/webp" srcset="https://events.grinnell.edu/live/image/scale/2x/gid/3/width/300/height/158/crop/1/96_BJJ.rev.1695405340.webp 2x, https://events.grinnell.edu/live/image/scale/3x/gid/3/width/300/height/158/crop/1/96_BJJ.rev.1695405340.webp 3x" data-origin="responsive">   <source type="image/jpeg" srcset="https://events.grinnell.edu/live/image/scale/2x/gid/3/width/300/height/158/crop/1/96_BJJ.rev.1695405340.jpg 2x, https://events.grinnell.edu/live/image/scale/3x/gid/3/width/300/height/158/crop/1/96_BJJ.rev.1695405340.jpg 3x" data-origin="responsive"> <img src="https://events.grinnell.edu/live/image/gid/3/width/300/height/158/crop/1/96_BJJ.rev.1695405340.jpg" width="300" height="158" alt="Brazilian Jiu-Jitsu" srcset="https://events.grinnell.edu/live/image/scale/2x/gid/3/width/300/height/158/crop/1/96_BJJ.rev.1695405340.jpg 2x, https://events.grinnell.edu/live/image/scale/3x/gid/3/width/300/height/158/crop/1/96_BJJ.rev.1695405340.jpg 3x" data-max-w="1180" data-max-h="620" loading="lazy" data-optimized="true"></picture>
<div class="lw_calendar_event_description"> <p>
  Brazilian Jiu-Jitsu class. Each class is self-contained and welcoming to beginners and advanced players. Classes consist of warm-up exercises and drills, learning of specific techniques and live rolling.&nbsp;
</p> </div>"""

msg_alternative = MIMEMultipart('alternative')
msg.attach(msg_alternative)

plain_text = MIMEText(text, "plain", 'utf-8')
html_text = MIMEText(html, "html", 'utf-8')
cal_ics =  MIMEText(ics_data, 'calendar', 'utf-8')
cal_ics.set_param('method', "REQUEST")

msg_alternative.attach(plain_text)
msg_alternative.attach(html_text)
msg_alternative.attach(cal_ics)

cal_ics_attachment = MIMEBase('text', 'calendar', method='REQUEST', name='invite.ics')
cal_ics_attachment.set_payload(cal.to_ical()) # Use the raw bytes directly here
encoders.encode_base64(cal_ics_attachment)
cal_ics_attachment.add_header('Content-Disposition', 'attachment; filename="invite.ics"')

msg.attach(cal_ics_attachment)

# print(msg.as_string())

smtp_server = "live.smtp.mailtrap.io"
port = 2525

try:
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login("api", API_KEY)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print('Invitation Delivery Success')
except Exception as e:
    print(f'Invitation Delivery Failure: {e}')
