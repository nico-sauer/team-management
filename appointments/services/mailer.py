from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .ics_generator import generate_ics
from email.utils import format_datetime
from datetime import datetime
import pytz


def send_booking_invite(booking, recipients):
    subject = f"Invitation: {booking.title}"
    from_email = settings.EMAIL_HOST_USER

    # Plaintext-version
    text_content = (
        f"You are invited to {booking.title}.\n\n"
        f"When: {booking.start} - {booking.end}\n"
        f"Where: {booking.location}"
    )

    # HTML-version
    html_content = f"""
    <html>
        <body>
            <h3>{booking.title}</h3>
            <p><b>When:</b> {booking.start} - {booking.end}</p>
            <p><b>Where:</b> {booking.location}</p>
        </body>
    </html>
    """

    # create email-object
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipients)
    msg.attach_alternative(html_content, "text/html")

    # attach ICS-attachment
    ics_content = generate_ics(booking)
    msg.attach("invite.ics", ics_content, "text/calendar")
    
    
    # set date header email head in timezone berlin
    berlin_tz = pytz.timezone("Europe/Berlin")
    now_berlin = datetime.now(berlin_tz)
    msg.extra_headers = {
        "Date": format_datetime(now_berlin)
    }

    # send booking email w/ attached ics file
    msg.send()





# def send_booking_invite(booking, to_email):
#     subject = f"Invitation: {booking.title}"
#     from_email = os.getenv("EMAIL_HOST_USER")

#     msg = MIMEMultipart("alternative")
#     msg["Subject"] = subject
#     msg["From"] = from_email
#     msg["To"] = to_email

#     # Text / HTML
#     text = f"You are invited to {booking.title}.\n\nWhen: {booking.start} - {booking.end}\nWhere: {booking.location}"
#     html = f"<html><body><p><b>{booking.title}</b></p><p>{booking.start} - {booking.end}</p><p>{booking.location}</p></body></html>"
#     msg.attach(MIMEText(text, "plain"))
#     msg.attach(MIMEText(html, "html"))

#     # ICS dynamisch erzeugen
#     ics_content = generate_ics(booking)
#     ics_attachment = MIMEApplication(ics_content, _subtype="ics")
#     ics_attachment.add_header("Content-Disposition", "attachment", filename="invite.ics")
#     msg.attach(ics_attachment)

#     # Mail verschicken
#     try:
#         server = smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT")))
#         server.starttls()
#         server.login(from_email, os.getenv("EMAIL_HOST_PASSWORD"))
#         server.sendmail(from_email, to_email, msg.as_string())
#         server.quit()
#         print("Invitation sent successfully!")
#     except Exception as error:
#         print(f"Error sending invitation: {error}")
