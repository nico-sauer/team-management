from django.utils import timezone
import pytz

def generate_ics(booking):
    """
    Generates an ICS calendar event for a booking.
    Times are converted to Europe/Berlin and TZID is used.
    """

    berlin_tz = pytz.timezone("Europe/Berlin")

    # Convert booking times to Berlin timezone
    start_berlin = booking.start.astimezone(berlin_tz)
    end_berlin = booking.end.astimezone(berlin_tz)
    dtstamp = timezone.now().astimezone(berlin_tz).strftime("%Y%m%dT%H%M%S")

    dtstart = start_berlin.strftime("%Y%m%dT%H%M%S")
    dtend = end_berlin.strftime("%Y%m%dT%H%M%S")
    
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//YourApp//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:{booking.id}@teamapp.com
DTSTAMP:{dtstamp}
DTSTART;TZID=Europe/Berlin:{dtstart}
DTEND;TZID=Europe/Berlin:{dtend}
SUMMARY:{booking.title}
LOCATION:{booking.location or ""}
DESCRIPTION:{booking.event_type or ""}
STATUS:{booking.status or "CONFIRMED"}
END:VEVENT
END:VCALENDAR"""

    return ics_content.encode("utf-8") # Returns bytes, ready to attach to email
