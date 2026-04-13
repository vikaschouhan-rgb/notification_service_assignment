from sqlalchemy import Column, Integer, String, DateTime
from datetime import UTC, datetime

from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    channel = Column(String)

    message = Column(String)

    priority = Column(String)

    status = Column(String,default="pending")

    retry_count = Column(Integer,default=0)

    created_at = Column(DateTime,default=datetime.now(UTC))

    recipient = Column(String)

    max_retries = Column(Integer, default=3)