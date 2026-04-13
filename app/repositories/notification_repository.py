from app.models import Notification


class NotificationRepository:

    def __init__(self, db):
        self.db = db

    def create_notification(self, data):
        notification = Notification(**data.model_dump())

        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)

        return notification

    def get_all_notifications(self):
        return self.db.query(Notification).all()