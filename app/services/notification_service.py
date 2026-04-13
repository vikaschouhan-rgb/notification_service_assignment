from app.repositories.notification_repository import NotificationRepository
from app.database import SessionLocal

from app.core.queue import notification_queue
from app.tasks.send_notification import send_notification

from datetime import timedelta

class NotificationService:

    def __init__(self, repository):
        self.repository = repository

    def create_notification(self, data):

        # Save to DB
        notification = self.repository.create_notification(data)

        print("DEBUG: Notification saved:", notification.id)

        # Enqueue job to Redis
        job = notification_queue.enqueue(
            send_notification,
            notification.id,
            notification.message,
            notification.priority,
            notification.channel
        )

        print("DEBUG: Job queued:", job.id)

        return notification

    def get_all_notifications(self):
        return self.repository.get_all_notifications()


db = SessionLocal()
repository = NotificationRepository(db)
notification_service = NotificationService(repository)