
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.settings import settings
from config.extensions.exception_handler import Unauthorized

def send_mail(to_email: str, subject: str, body: str):
    sender_email = settings.MAIL_SENDER
    smtp_server = settings.MAIL_HOST
    smtp_port = settings.MAIL_PORT
    smtp_password = settings.MAIL_PASSWORD

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, smtp_password)  # Log in to the SMTP server
            server.sendmail(sender_email, to_email, msg.as_string())  # Send the email
    except smtplib.SMTPAuthenticationError:
        return Unauthorized(message='SMTP Authentication failed. Check username/password.')
    