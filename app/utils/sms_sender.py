# from app.core.twilio_config import (
#     client,
#     twilio_phone_number,
# )


# def send_sms_notification(message):

#     client.messages.create(
#         body=message,
#         from_=twilio_phone_number,
#         to="+918827166782",
#     )


import os

from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


def send_sms_notification(recipient, message):

    try:
        account_sid = ("ACXXXXXXXXXXXXXXXX")
        auth_token = ("13412341243")
        from_number = ("+1234567890")

        client = Client(account_sid, auth_token)

        sms = client.messages.create(
            body=message,
            from_=from_number,
            to=recipient
        )

        print("SMS sent. SID:", sms.sid)

    except Exception as e:

        print("SMS failed:", e)
        raise