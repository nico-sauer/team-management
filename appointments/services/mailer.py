from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.conf import settings
from .ics_generator import generate_ics
from email.utils import format_datetime
from datetime import datetime
import pytz


def send_booking_invite(booking, recipients, generate_only=False, instance=None):
    """
    If generate_only=True, only the ICS file is generated and returned.
    Otherwise, it is sent directly as before.
    """
    ics_content = generate_ics(booking)
    if generate_only:
        from io import BytesIO
        if isinstance(ics_content, str):
            ics_content = ics_content.encode("utf-8")

        ics_io = BytesIO(ics_content)
        return ics_io

    # Standard mail 
    email = EmailMessage(
        subject=f"Invitation: {booking.title}",
        body=f"Appointment: '{booking.title}'.",
        to=recipients,
    )
    email.attach("invitation.ics", ics_content, "text/calendar")
    email.send()



#-- send ics.file automatically

# def send_booking_invite(booking, recipients):
#     subject = f"Invitation: {booking.title}"
#     from_email = settings.EMAIL_HOST_USER

#     # Plaintext-version
#     text_content = (
#         f"You are invited to {booking.title}.\n\n"
#         f"When: {booking.start} - {booking.end}\n"
#         f"Where: {booking.location}"
#     )

#     # HTML-version
#     html_content = f"""
#     <html>
#         <body>
#             <h3>{booking.title}</h3>
#             <p><b>When:</b> {booking.start} - {booking.end}</p>
#             <p><b>Where:</b> {booking.location}</p>
#         </body>
#     </html>
#     """

#     # create email-object
#     msg = EmailMultiAlternatives(subject, text_content, from_email, recipients)
#     msg.attach_alternative(html_content, "text/html")

#     # attach ICS-attachment (with charset & method for gmail etc.)
#     ics_content = generate_ics(booking)
#     msg.attach(
#         "invite.ics", ics_content, "text/calendar;" " charset=UTF-8; method=REQUEST"
#     )

#     # set date header email head in timezone berlin
#     berlin_tz = pytz.timezone("Europe/Berlin")
#     now_berlin = datetime.now(berlin_tz)
#     msg.extra_headers = {"Date": format_datetime(now_berlin)}

#     # send booking email w/ attached ics file
#     msg.send()
