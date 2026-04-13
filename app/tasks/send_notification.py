import asyncio
from datetime import timedelta

from app.core import sns_service
from app.database import SessionLocal
from app.models.notification import Notification
from app.utils.email_sender import send_email_notification
from app.utils.push_sender import send_push_notification
from app.utils.sms_sender import send_sms_notification
from app.core.queue import notification_queue


def send_notification(notification_id, message, priority, channel):

    db = SessionLocal()

    notification = db.query(Notification).get(notification_id)

    try:
        print(f"Processing notification ID={notification_id}")

        notification.status = "processing"
        db.commit()

        if channel == "email":
            asyncio.run(
                send_email_notification(
                    notification.recipient,
                    notification.message
                )
            )

            notification.status = "sent"
            db.commit()
            print("Email sent")
            
        elif channel == "sms":
            send_sms_notification(
                notification.recipient,
                notification.message
            )

            notification.status = "sent"
            db.commit()
            print("SMS sent")
            
        elif channel == "push":
            send_push_notification(
                notification.recipient,   
                notification.message
            )

            notification.status = "sent"
            db.commit()
            print("Push sent")

        else:
            notification.status = "failed"
            db.commit()
            print("Unknown channel")

    except Exception as e:
        print("Error:", e)
        notification.retry_count += 1

        if notification.retry_count < notification.max_retries:
            print(
                f"Retrying... attempt "
                f"{notification.retry_count}"
            )
            notification.status = "retrying"
            db.commit()
            notification_queue.enqueue_in(
                timedelta(seconds=10),
                send_notification,
                notification.id,
                notification.message,
                notification.priority,
                notification.channel,
            )

        else:
            notification.status = "failed"
            db.commit()
            print("Max retries reached")

    finally:
        db.close()