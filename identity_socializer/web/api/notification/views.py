from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from mongoengine import connect

from identity_socializer.db.collections.notifications import (
    get_all_notifications,
    get_messages_by_user_id,
)
from identity_socializer.db.dao.push_token_dao import PushTokenDAO
from identity_socializer.db.dao.user_dao import UserDAO
from identity_socializer.services.push_notifications import PushNotifications
from identity_socializer.settings import settings
from identity_socializer.web.api.notification.schema import (
    NotificationDTO,
    NotificationSchema,
    TrendingNotificationDTO,
)

router = APIRouter()

# Create connection to mongo db
connect(
    db="identity_socializer",
    host=settings.mongo_host,
    port=27017,
)


@router.get("/get_all", response_model=None)
async def new_all_notifications() -> Any:
    """Creates a notification for new like event."""
    my_notifications = []
    notifications = get_all_notifications()

    for notification in notifications:

        notif = NotificationSchema(
            id=str(notification.id),
            user_id=notification.user_id,
            title=notification.title,
            content=notification.content,
            notification_type=notification.notification_type,
            redirect_id=notification.redirect_id,
            created_at=str(notification.created_at),
        )

        my_notifications.append(notif)

    return my_notifications


@router.post("/new_trending_snap", response_model=None)
async def new_trending_snap_notification(
    body: TrendingNotificationDTO,
    user_dao: UserDAO = Depends(),
    push_token_dao: PushTokenDAO = Depends(),
    push_notifications: PushNotifications = Depends(),
) -> None:
    """Creates a notification for new like event."""
    await push_notifications.new_trending_snap(
        body.topic,
        body.snap,
        user_dao,
        push_token_dao,
    )


@router.post("/new_like", response_model=None)
async def new_like_notification(
    body: NotificationDTO,
    user_dao: UserDAO = Depends(),
    push_token_dao: PushTokenDAO = Depends(),
    push_notifications: PushNotifications = Depends(),
) -> None:
    """Creates a notification for new like event."""
    await push_notifications.new_like(
        body.from_id,
        body.to_id,
        body.snap,
        user_dao,
        push_token_dao,
    )


@router.post("/new_mention", response_model=None)
async def new_mention_notification(
    body: NotificationDTO,
    user_dao: UserDAO = Depends(),
    push_token_dao: PushTokenDAO = Depends(),
    push_notifications: PushNotifications = Depends(),
) -> None:
    """Creates a notification for new mention event."""
    await push_notifications.new_mention(
        body.from_id,
        body.to_id,
        body.snap,
        user_dao,
        push_token_dao,
    )


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
                notification_type=notification.notification_type,
                redirect_id=notification.redirect_id,
                created_at=str(notification.created_at),
            )

            my_notifications.append(notif)

        return my_notifications

    except Exception as error:
        code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(error))
