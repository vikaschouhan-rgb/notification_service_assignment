import asyncio

from fastapi_mail import FastMail, MessageSchema

from app.core.email_config import conf


async def send_email_notification(recipient, message):

    email = MessageSchema(
        subject="Notification",
        recipients=[recipient],
        body=message,
        subtype="plain",
    )

    fm = FastMail(conf)

    await fm.send_message(email)