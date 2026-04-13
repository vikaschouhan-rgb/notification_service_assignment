import os
import logging

from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def send_sms_notification(recipient, message):
    try:
        logger.info(f"Preparing SMS for recipient={recipient}")

        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_PHONE_NUMBER")

        if not all([account_sid, auth_token, from_number]):
            logger.error("Twilio configuration missing")
            raise ValueError("Twilio credentials not properly set")

        client = Client(account_sid, auth_token)

        logger.info(f"Sending SMS to {recipient}")

        sms = client.messages.create(
            body=message,
            from_=from_number,
            to=recipient
        )

        logger.info(f"SMS sent successfully to {recipient}, SID={sms.sid}")

        return sms.sid

    except Exception as e:
        logger.error(
            f"SMS failed for recipient={recipient}: {str(e)}",
            exc_info=True
        )
        raise
