import os
from qna_api.crosscutting.logging import get_logger

logger = get_logger(__name__)

class NotificationService:
    def __init__(self, api_key: str, sender_email: str):
        self.api_key = api_key
        self.sender_email = sender_email
        
    def send_email_verification(self, email: str, verification_url: str):
        logger.info(f"Sending email verification to {email} with URL: {verification_url}")
    
    @classmethod
    def from_env_vars(cls):
        api_key = os.getenv('NOTIFICATION_API_KEY', 'dummy_api_key')
        sender_email = os.getenv('NOTIFICATION_SENDER_EMAIL', 'no-reply@example.com')
        return cls(api_key, sender_email)