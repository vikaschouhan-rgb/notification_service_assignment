import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.notification import Notification
from app.models import UserPreference

from app.schemas.notification_schema import (
    NotificationCreate,
    NotificationResponse,
    PreferencesRequest,
    PreferencesResponse,
)

from app.services.notification_service import notification_service

# Logger setup
logger = logging.getLogger(__name__)

router = APIRouter()


def map_preferences(pref: UserPreference):
    return PreferencesResponse(
        user_id=pref.user_id,
        email=pref.email_enabled,
        sms=pref.sms_enabled,
        push=pref.push_enabled
    )


# -------------------------------------------------
# 1) POST /notifications
# -------------------------------------------------
@router.post("/notifications", response_model=NotificationResponse, status_code=201)
def create_notification(request: NotificationCreate):
    try:
        notification = notification_service.create_notification(request)
        logger.info(f"Notification created for user_id={request.user_id}")
        return notification

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Internal error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


# -------------------------------------------------
# 2) GET /notifications
# -------------------------------------------------
@router.get("/notifications", response_model=List[NotificationResponse])
def get_notifications():
    try:
        data = notification_service.get_all_notifications()
        logger.info("Fetched all notifications")
        return data

    except Exception as e:
        logger.error(f"Error fetching notifications: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


# -------------------------------------------------
# 3) GET /notifications/{id}
# -------------------------------------------------
@router.get("/notifications/{notification_id}", response_model=NotificationResponse)
def get_notification_status(notification_id: int, db: Session = Depends(get_db)):
    try:
        notification = (
            db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

        if not notification:
            logger.warning(f"Notification {notification_id} not found")
            raise HTTPException(status_code=404, detail="Notification not found")

        return notification

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error fetching notification {notification_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


# -------------------------------------------------
# 4) GET /users/{user_id}/notifications
# -------------------------------------------------
@router.get("/users/{user_id}/notifications", response_model=List[NotificationResponse])
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    try:
        notifications = (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

        logger.info(f"Fetched notifications for user_id={user_id}")
        return notifications

    except Exception as e:
        logger.error(f"Error fetching user notifications: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


# -------------------------------------------------
# 5) POST /users/{user_id}/preferences
# -------------------------------------------------
@router.post("/users/{user_id}/preferences", response_model=PreferencesResponse)
def set_user_preferences(
    user_id: int,
    request: PreferencesRequest,
    db: Session = Depends(get_db)
):
    try:
        preferences = (
            db.query(UserPreference)
            .filter(UserPreference.user_id == user_id)
            .first()
        )

        if preferences:
            preferences.email_enabled = request.email
            preferences.sms_enabled = request.sms
            preferences.push_enabled = request.push
            logger.info(f"Updated preferences for user_id={user_id}")
        else:
            preferences = UserPreference(
                user_id=user_id,
                email_enabled=request.email,
                sms_enabled=request.sms,
                push_enabled=request.push
            )
            db.add(preferences)
            logger.info(f"Created preferences for user_id={user_id}")

        db.commit()
        db.refresh(preferences)

        return map_preferences(preferences)

    except Exception as e:
        db.rollback()
        logger.error(f"Error setting preferences: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


# -------------------------------------------------
# 6) GET /users/{user_id}/preferences
# -------------------------------------------------
@router.get("/users/{user_id}/preferences", response_model=PreferencesResponse)
def get_user_preferences(user_id: int, db: Session = Depends(get_db)):
    try:
        preferences = (
            db.query(UserPreference)
            .filter(UserPreference.user_id == user_id)
            .first()
        )

        if not preferences:
            logger.warning(f"Preferences not found for user_id={user_id}")
            raise HTTPException(status_code=404, detail="User preferences not found")

        return map_preferences(preferences)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error fetching preferences: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
