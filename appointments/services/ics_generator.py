from django.utils import timezone
import pytz
from config import settings


def generate_ics(booking, instance=None):
    """
    Generates a fully RFC 5545-compliant ICS event.
    Supports both Booking and BookingInstance.
    Compatible with Gmail, Outlook, iOS, Android.
    """

    berlin_tz = pytz.timezone("Europe/Berlin")

    # Use instance data if available
    if instance:
        title = instance.current_title
        start = instance.current_start.astimezone(berlin_tz)
        end = instance.current_end.astimezone(berlin_tz)
        uid = f"{booking.id}-{instance.occurrence_date}@teamapp.com"
    else:
        title = booking.title
        start = booking.start.astimezone(berlin_tz)
        end = booking.end.astimezone(berlin_tz)
        uid = f"{booking.id}@teamapp.com"

    dtstamp = timezone.now().astimezone(berlin_tz).strftime("%Y%m%dT%H%M%S")
    dtstart = start.strftime("%Y%m%dT%H%M%S")
    dtend = end.strftime("%Y%m%dT%H%M%S")

    # Timezone block for Gmail & Outlook compatibility
    VTIMEZONE = """BEGIN:VTIMEZONE
TZID:Europe/Berlin
X-LIC-LOCATION:Europe/Berlin
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE"""

    organizer_email = settings.EMAIL_HOST_USER
    user = getattr(booking, "booked_by", None)
    attendee_email = getattr(user, "email", None) or "guest@example.com"

    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//YourApp//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
{VTIMEZONE}
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART;TZID=Europe/Berlin:{dtstart}
DTEND;TZID=Europe/Berlin:{dtend}
SUMMARY:{title}
LOCATION:{booking.location or ""}
DESCRIPTION:{booking.event_type or ""}
STATUS:{booking.status.upper() if booking.status else "CONFIRMED"}
ORGANIZER;CN=TeamApp:mailto:{organizer_email}
ATTENDEE;CN=Guest;RSVP=TRUE:mailto:{attendee_email}
END:VEVENT
END:VCALENDAR"""

    # Gmail expects CRLF line endings
    return ics_content.replace("\n", "\r\n").encode("utf-8")
