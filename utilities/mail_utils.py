import settings
import smtplib
from email.message import EmailMessage


def send_mail(from_email: str, subject: str, message: str, use_ssl=True):
    # TODO: https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python
    # Set up gmail account using this instructions, to check it works run test_mail_sender.py
    # Or run SMTP server locally and set in the .env file to the LOCAL host and post. more info in test_mail_sender.py
    msg = EmailMessage()
    msg['Subject'] = f"{from_email} --- {subject}"
    msg['From'] = settings.CONTACT_EMAIL
    msg['To'] = ', '.join([settings.CONTACT_EMAIL])
    msg.set_content(message)

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            if use_ssl:
                server.starttls()
                server.login(settings.CONTACT_EMAIL, settings.CONTACT_EMAIL_PASSWORD)

            server.sendmail(settings.CONTACT_EMAIL, settings.CONTACT_EMAIL,  msg.as_string())
            print('successfully sent the mail.')
    except Exception:
        print('Failed sending email')

