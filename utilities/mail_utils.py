import settings
import smtplib
from email.message import EmailMessage


def send_mail(email: str, subject: str, message: str):
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.login(settings.CONTACT_EMAIL, settings.CONTACT_EMAIL_PASSWORD)
    server.sendmail(settings.CONTACT_EMAIL, email, message)

