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

router = APIRouter()


# -------------------------------------------------
# Helper: Map DB -> Response Schema
# -------------------------------------------------
# def map_preferences(pref: UserPreference) -> PreferencesResponse:
#     return PreferencesResponse(
#         user_id=pref.user_id,
#         email=pref.email_enabled,
#         sms=pref.sms_enabled,
#         push=pref.push_enabled
#     )

def map_preferences(pref: UserPreference):
    return PreferencesResponse(
        user_id=pref.user_id,
        email=pref.email_enabled,
        sms=pref.sms_enabled,
        push=pref.push_enabled
    )


# -------------------------------------------------
# 1) POST /notifications
# Create notification
# -------------------------------------------------
@router.post(
    "/notifications",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_notification(request: NotificationCreate):
    notification = notification_service.create_notification(request)
    return notification


# -------------------------------------------------
# 2) GET /notifications
# Get all notifications
# -------------------------------------------------
@router.get(
    "/notifications",
    response_model=List[NotificationResponse],
    status_code=status.HTTP_200_OK
)
def get_notifications():
    return notification_service.get_all_notifications()


# -------------------------------------------------
# 3) GET /notifications/{id}
# Get notification status
# -------------------------------------------------
@router.get(
    "/notifications/{notification_id}",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK
)
def get_notification_status(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return notification


# -------------------------------------------------
# 4) GET /users/{user_id}/notifications
# Get user notification history
# -------------------------------------------------
@router.get(
    "/users/{user_id}/notifications",
    response_model=List[NotificationResponse],
    status_code=status.HTTP_200_OK
)
def get_user_notifications(
    user_id: int,
    db: Session = Depends(get_db)
):
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return notifications  # empty list is OK


# -------------------------------------------------
# 5) POST /users/{user_id}/preferences
# Create or update user preferences
# -------------------------------------------------
@router.post(
    "/users/{user_id}/preferences",
    response_model=PreferencesResponse,
    status_code=status.HTTP_200_OK
)
def set_user_preferences(
    user_id: int,
    request: PreferencesRequest,
    db: Session = Depends(get_db)
):
    preferences = (
        db.query(UserPreference)
        .filter(UserPreference.user_id == user_id)
        .first()
    )

    if preferences:
        # Update
        preferences.email_enabled = request.email
        preferences.sms_enabled = request.sms
        preferences.push_enabled = request.push
    else:
        # Create
        preferences = UserPreference(
            user_id=user_id,
            email_enabled=request.email,
            sms_enabled=request.sms,
            push_enabled=request.push
        )
        db.add(preferences)

    db.commit()
    db.refresh(preferences)

    return map_preferences(preferences)


# -------------------------------------------------
# 6) GET /users/{user_id}/preferences
# Get user preferences
# -------------------------------------------------
@router.get(
    "/users/{user_id}/preferences",
    response_model=PreferencesResponse,
    status_code=status.HTTP_200_OK
)
def get_user_preferences(
    user_id: int,
    db: Session = Depends(get_db)
):
    preferences = (
        db.query(UserPreference)
        .filter(UserPreference.user_id == user_id)
        .first()
    )

    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found"
        )

    return map_preferences(preferences)

# -------------------------------------------------
# IMPORTANT: Add preference check before sending
# -------------------------------------------------

# def check_user_channel_enabled(user_id: int, channel: str, db: Session):
#     preferences = (
#         db.query(UserPreferences)
#         .filter(UserPreferences.user_id == user_id)
#         .first()
#     )

#     if not preferences:
#         return True

#     if channel == "email" and not preferences.email:
#         return False

#     if channel == "sms" and not preferences.sms:
#         return False

#     if channel == "push" and not preferences.push:
#         return False

#     return True

