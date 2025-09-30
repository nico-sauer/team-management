from django.core.mail import send_mail
from django.conf import settings
from pathlib import Path

def test_console_email():
    """
    Tests the Console backend.
    The email will be printed to the terminal.
    """
    original_backend = settings.EMAIL_BACKEND
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    print("\n=== Console Email Test ===")
    send_mail(
        subject="Console Backend Test",
        message="This is a test email using the Console backend.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["test@example.com"]
    )
    settings.EMAIL_BACKEND = original_backend


def test_filebased_email():
    """
    Tests the File-based backend.
    The email will be saved as a .eml file in the specified folder.
    """
    original_backend = settings.EMAIL_BACKEND
    original_path = getattr(settings, "EMAIL_FILE_PATH", None)

    # Test path
    test_folder = Path(settings.BASE_DIR) / "appointments" / "sent_emails_test"
    test_folder.mkdir(parents=True, exist_ok=True)

    settings.EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    settings.EMAIL_FILE_PATH = test_folder

    print("\n=== Filebased Email Test ===")
    send_mail(
        subject="Filebased Backend Test",
        message="This is a test email using the Filebased backend.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["test@example.com"]
    )

    print(f"The email should now exist in the folder: {test_folder.resolve()}")

    # Restore original settings
    settings.EMAIL_BACKEND = original_backend
    if original_path:
        settings.EMAIL_FILE_PATH = original_path


def test_smtp_email():
    """
    Tests the SMTP backend.
    The email will be actually sent, SMTP settings must be correct.
    """
    original_backend = settings.EMAIL_BACKEND
    settings.EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    print("\n=== SMTP Email Test ===")
    send_mail(
        subject="SMTP Backend Test",
        message="This is a test email using the SMTP backend.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["brittaktb@web.de"]
    )

    print("The email should have been sent (check the mailbox).")

    # Restore original settings
    settings.EMAIL_BACKEND = original_backend


if __name__ == "__main__":
    print("Starting email tests...")
    test_console_email()
    test_filebased_email()
    test_smtp_email()
    print("Email tests completed.")


# test 
# from appointments.models import Booking
# from appointments.services.mailer import send_booking_invite

# # load the first appointment booking
# booking = Booking.objects.first()

# # send test mail to registered email 
# send_booking_invite(booking, ["brittaktb@web.de"])