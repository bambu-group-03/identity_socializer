from typing import List

from fastapi import APIRouter, HTTPException, status
from mongoengine import connect

from identity_socializer.db.collections.notifications import (
    create_notification,
    get_messages_by_user_id,
)
from identity_socializer.settings import settings
from identity_socializer.web.api.notification.schema import (
    NotificationDTO,
    NotificationSchema,
)

router = APIRouter()

# Create connection to mongo db
connect(
    db="identity_socializer",
    host=settings.mongo_host,
    port=27017,
)


@router.post("/", response_model=None)
def new_notification(
    body: NotificationDTO,
) -> NotificationSchema:
    """
    Creates a notification with the given body.

    :raises HTTPException: If something goes wrong.
    """
    try:
        notification = create_notification(
            user_id=body.user_id,
            title=body.title,
            content=body.content,
        )

        return NotificationSchema(
            id=str(notification.id),
            user_id=notification.user_id,
            title=notification.title,
            content=notification.content,
            created_at=str(notification.created_at),
        )

    except Exception as error:
        code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(error))


@router.get("/{user_id}", response_model=None)
def get_notifications_by_user_id(
    user_id: str,
) -> List[NotificationSchema]:
    """
    Get notifications for a given user.

    :raises HTTPException: If something goes wrong.
    """
    try:
        my_notifications = []
        notifications = get_messages_by_user_id(user_id)

        for notification in notifications:

            notif = NotificationSchema(
                id=str(notification.id),
                user_id=notification.user_id,
                title=notification.title,
                content=notification.content,
                created_at=str(notification.created_at),
            )

            my_notifications.append(notif)

        return my_notifications

    except Exception as error:
        code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(error))
