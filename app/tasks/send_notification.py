import asyncio
import logging
from datetime import timedelta

from app.core import sns_service
from app.database import SessionLocal
from app.models.notification import Notification
from app.utils.email_sender import send_email_notification
from app.utils.push_sender import send_push_notification
from app.utils.sms_sender import send_sms_notification
from app.core.queue import notification_queue

logger = logging.getLogger(__name__)


def send_notification(notification_id, message, priority, channel):
    db = SessionLocal()

    try:
        logger.info(f"Starting processing notification_id={notification_id}")

        notification = db.query(Notification).get(notification_id)

        if not notification:
            logger.error(f"Notification not found: id={notification_id}")
            return

        notification.status = "processing"
        db.commit()

        # ---------------- CHANNEL HANDLING ----------------
        if channel == "email":
            logger.info(f"Sending EMAIL to {notification.recipient}")

            asyncio.run(
                send_email_notification(
                    notification.recipient,
                    notification.message
                )
            )

            notification.status = "sent"
            db.commit()
            logger.info(f"Email sent successfully for id={notification_id}")

        elif channel == "sms":
            logger.info(f"Sending SMS to {notification.recipient}")

            send_sms_notification(
                notification.recipient,
                notification.message
            )

            notification.status = "sent"
            db.commit()
            logger.info(f"SMS sent successfully for id={notification_id}")

        elif channel == "push":
            logger.info(f"Sending PUSH to {notification.recipient}")

            send_push_notification(
                notification.recipient,
                notification.message
            )

            notification.status = "sent"
            db.commit()
            logger.info(f"Push sent successfully for id={notification_id}")

        else:
            logger.warning(f"Unknown channel '{channel}' for id={notification_id}")
            notification.status = "failed"
            db.commit()

    except Exception as e:
        logger.error(
            f"Error processing notification_id={notification_id}: {str(e)}",
            exc_info=True
        )

        notification.retry_count += 1

        if notification.retry_count < notification.max_retries:
            logger.warning(
                f"Retrying notification_id={notification_id}, "
                f"attempt={notification.retry_count}"
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

            logger.error(
                f"Max retries reached for notification_id={notification_id}"
            )

    finally:
        db.close()
        logger.info(f"DB session closed for notification_id={notification_id}")
