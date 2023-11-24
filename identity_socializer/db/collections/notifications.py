from datetime import datetime
from typing import List

from mongoengine import DateTimeField, Document, StringField


class Notification(Document):
    """Schema for Notification."""

    user_id = StringField(required=True)
    title = StringField(required=True)
    content = StringField()
    created_at = DateTimeField(default=lambda: datetime.now())

    meta = {
        "collection": "notifications",
    }


def create_notification(
    user_id: str,
    title: str,
    content: str,
) -> Notification:
    """Create a notification in mongo db."""
    new_notification = Notification(
        user_id=user_id,
        title=title,
        content=content,
    )
    new_notification.save()

    return new_notification


def get_messages_by_user_id(user_id: str) -> List[Notification]:
    """Get messages by chat id."""
    return Notification.objects(user_id=user_id).order_by("-created_at")
