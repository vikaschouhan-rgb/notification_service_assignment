from sqlalchemy import Column, Integer, Boolean

from app.database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    email_enabled = Column(Boolean, default=True)

    sms_enabled = Column(Boolean, default=True)

    push_enabled = Column(Boolean, default=True)