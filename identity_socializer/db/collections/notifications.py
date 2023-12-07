from datetime import datetime
from typing import List, Optional

from mongoengine import DateTimeField, Document, StringField


class Notification(Document):
    """Schema for Notification."""

    user_id = StringField(required=True)
    title = StringField(required=True)
    content = StringField()
    notification_type = StringField(required=False)
    redirect_id = StringField(required=False)
    created_at = DateTimeField(default=lambda: datetime.now())

    meta = {
        "collection": "notifications",
    }


def create_notification(
    user_id: str,
    title: str,
    content: str,
    notification_type: Optional[str] = None,
    redirect_id: Optional[str] = None,
) -> Notification:
    """Create a notification in mongo db."""
    new_notification = Notification(
        user_id=user_id,
        title=title,
        content=content,
        notification_type=notification_type,
        redirect_id=redirect_id,
    )
    new_notification.save()

    return new_notification


def get_messages_by_user_id(user_id: str) -> List[Notification]:
    """Get messages by chat id."""
    return Notification.objects(user_id=user_id).order_by("-created_at")


def get_all_notifications() -> List[Notification]:
    """Get all notifications."""
    return Notification.objects().order_by("-created_at")
