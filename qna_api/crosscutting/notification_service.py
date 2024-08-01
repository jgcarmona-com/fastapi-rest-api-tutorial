import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from qna_api.crosscutting.logging import get_logger

logger = get_logger(__name__)

class NotificationService:
    def __init__(self, smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str, sender_email: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.sender_email = sender_email
        
    @classmethod
    def from_env_vars(cls):
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 465))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        sender_email = os.getenv('SENDER_EMAIL', smtp_username)
        return cls(smtp_server, smtp_port, smtp_username, smtp_password, sender_email)
    
    async def send_email_verification(self, recipient_email: str, verification_url: str):
        use_smtp = os.getenv('USE_SMTP', 'false').lower() == 'true'
        if not use_smtp:
            logger.warn("SMTP not configured. Users require admin validation.")
            return False  # Indicate that email was not sent
        
        logger.info(f"Sending email verification to {recipient_email} with URL: {verification_url}")
        message = MIMEMultipart("alternative")
        message["Subject"] = "Email Verification"
        message["From"] = self.sender_email
        message["To"] = recipient_email

        text = f"Please verify your email by clicking on the following link: {verification_url}"
        html = f"<html><body><p>Please verify your email by clicking on the following link: <a href='{verification_url}'>Verify Email</a></p></body></html>"

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            logger.info(f"Email sent to {recipient_email}")
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")

