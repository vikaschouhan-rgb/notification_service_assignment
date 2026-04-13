import asyncio
import logging

from fastapi_mail import FastMail, MessageSchema
from app.core.email_config import conf

logger = logging.getLogger(__name__)


async def send_email_notification(recipient, message):
    try:
        logger.info(f"Preparing email for recipient={recipient}")

        email = MessageSchema(
            subject="Notification",
            recipients=[recipient],
            body=message,
            subtype="plain",
        )

        fm = FastMail(conf)

        logger.info(f"Sending email to {recipient}")

        await fm.send_message(email)

        logger.info(f"Email sent successfully to {recipient}")

    except Exception as e:
        logger.error(
            f"Failed to send email to {recipient}: {str(e)}",
            exc_info=True
        )
        raise
