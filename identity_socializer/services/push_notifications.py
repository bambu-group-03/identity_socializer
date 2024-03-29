import json
from typing import Any, Optional

import httpx
from mongoengine import connect

from identity_socializer.db.collections.chats import get_chat_by_id
from identity_socializer.db.collections.notifications import create_notification
from identity_socializer.db.dao.push_token_dao import PushTokenDAO
from identity_socializer.db.dao.relationship_dao import RelationshipDAO
from identity_socializer.db.dao.user_dao import UserDAO
from identity_socializer.settings import settings
from identity_socializer.web.api.auth.schema import AppUserModel
from identity_socializer.web.api.auth.views import get_user_model

connect(
    db="identity_socializer",
    host=settings.mongo_host,
    port=27017,
)


class PushNotifications:
    """Class for sending push notifications."""

    def send(self, notification: Any) -> None:
        """Send push notification to user."""
        print(f"Sending push notification: {notification}")
        try:
            httpx.post(
                "https://exp.host/--/api/v2/push/send",
                json=notification,
            )
        except Exception as e:
            print(f"Fail to send push notification: {e}")
            print(e)

    def save_notification(
        self,
        user_id: str,
        title: str,
        content: str,
        notif_type: Optional[str] = None,
        redirect_id: Optional[str] = None,
    ) -> None:
        """Save notification to database."""
        create_notification(
            user_id=user_id,
            title=title,
            content=content,
            notification_type=notif_type,
            redirect_id=redirect_id,
        )

    async def new_trending_snap(
        self,
        topic_title: str,
        snap: Any,
        user_dao: UserDAO,
        push_token_dao: PushTokenDAO,
    ) -> None:
        """Send push notification for new trending topic snap."""
        # Create and save notification to database
        title = f"There's a new tweet about {topic_title}!"
        body = "Tap to join the conversation."
        notif_type = "NewTrendingNotification"

        users = await user_dao.get_all_users(limit=300, offset=0)
        for user in users:
            print(user)
            self.save_notification(
                user.id,
                title,
                body,
                notif_type,
                snap["id"],
            )

            # Send push notification to user
            push_tokens = await push_token_dao.get_push_tokens_by_user(user.id)

            for push_token in push_tokens:

                data = {
                    "screen": notif_type,
                    "params": {"snap": snap},
                }

                notification = _create_push_notification(push_token, title, body, data)

                self.send(notification)

    async def new_like(
        self,
        from_id: str,
        to_id: str,
        snap: Any,
        user_dao: UserDAO,
        push_token_dao: PushTokenDAO,
    ) -> None:
        """Send push notification for new like."""
        username = await user_dao.get_username_by_id(from_id) or "unknown"

        # Create and save notification to database
        title = "Your snap have a new like!"
        body = f"@{username} liked your snap!"
        notif_type = "NewLikeNotification"

        self.save_notification(to_id, title, body, notif_type, snap["id"])

        # Send push notification to user
        push_tokens = await push_token_dao.get_push_tokens_by_user(to_id)

        for push_token in push_tokens:
            data = {
                "screen": notif_type,
                "params": {"snap": snap},
            }

            notification = _create_push_notification(push_token, title, body, data)

            self.send(notification)

    async def new_reply(
        self,
        from_id: str,
        to_id: str,
        snap: Any,
        user_dao: UserDAO,
        push_token_dao: PushTokenDAO,
    ) -> None:
        """Send push notification for new reply."""
        username = await user_dao.get_username_by_id(from_id) or "unknown"

        # Create and save notification to database
        title = "Your snap have a new reply!"
        body = f"@{username} replied your snap!"
        notif_type = "NewCommentNotification"

        self.save_notification(to_id, title, body, notif_type, snap["id"])

        # Send push notification to user
        push_tokens = await push_token_dao.get_push_tokens_by_user(to_id)

        for push_token in push_tokens:
            data = {
                "screen": notif_type,
                "params": {"snap": snap},
            }

            notification = _create_push_notification(push_token, title, body, data)

            self.send(notification)

    async def new_follower(
        self,
        from_id: str,
        to_id: str,
        user_dao: UserDAO,
        relationship_dao: RelationshipDAO,
        push_token_dao: PushTokenDAO,
    ) -> None:
        """Send push notification for new follower."""
        user = await get_user_model(to_id, from_id, user_dao, relationship_dao)

        if user is None:
            return

        # Create and save notification to database
        title = "You have a new follower!"
        body = f"@{user.username} is following you!"
        notif_type = "NewFollowerNotification"

        self.save_notification(to_id, title, body, notif_type, user.id)

        # Send push notification to user
        push_tokens = await push_token_dao.get_push_tokens_by_user(to_id)
        for push_token in push_tokens:

            data = {
                "screen": notif_type,
                "params": {"user": _user_json_format(user)},
            }

            notification = _create_push_notification(push_token, title, body, data)

            self.send(notification)

    async def new_mention(
        self,
        from_id: str,
        to_id: str,
        snap: Any,
        user_dao: UserDAO,
        push_token_dao: PushTokenDAO,
    ) -> None:
        """Send push notification for new mention."""
        username = await user_dao.get_username_by_id(from_id) or "unknown"

        # Create and save notification to database
        title = "You have a new mention!"
        body = f"@{username} mentioned you!"
        notif_type = "NewMentionNotification"

        self.save_notification(to_id, title, body, notif_type, snap["id"])

        # Send push notification to user
        push_tokens = await push_token_dao.get_push_tokens_by_user(to_id)
        for push_token in push_tokens:

            data = {
                "screen": notif_type,
                "params": {"snap": snap},
            }

            notification = _create_push_notification(push_token, title, body, data)

            self.send(notification)

    async def new_message(
        self,
        from_id: str,
        to_id: str,
        chat_to_id: str,
        user_dao: UserDAO,
        relationship_dao: RelationshipDAO,
        push_token_dao: PushTokenDAO,
    ) -> None:
        """Send push notification for new message."""
        user = await get_user_model(to_id, from_id, user_dao, relationship_dao)

        if user is None:
            return

        chat = get_chat_by_id(chat_to_id)

        if chat is None:
            return

        chat_dict = {
            "id": str(chat.id),
            "owner_id": chat.owner_id,
            "other_id": chat.other_id,
            "created_at": str(chat.created_at),
        }

        # Create and save notification to database
        title = "You have a new message!"
        body = f"@{user.username} sent you a message!"
        notif_type = "NewMessageNotification"

        # Prepare notification data
        notification_data = {
            "screen": notif_type,
            "params": {
                "chat": chat_dict,
                "user": _user_json_format(user),
            },
        }

        self.save_notification(to_id, title, body, notif_type, str(chat.id))

        # Send push notification to user
        push_tokens = await push_token_dao.get_push_tokens_by_user(to_id)
        for push_token in push_tokens:
            notification = _create_push_notification(
                push_token,
                title,
                body,
                notification_data,
            )
            self.send(notification)


def _create_push_notification(push_token: str, title: str, body: str, data: Any) -> Any:
    """Create a push notification in a JSON serializable format."""
    # Ensure data is JSON serializable
    serialized_data = json.loads(json.dumps(data, default=str))

    return {
        "to": push_token,
        "sound": "default",
        "title": title,
        "body": body,
        "data": serialized_data,
    }


def _user_json_format(user: AppUserModel) -> Any:
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone_number,
        "bio_msg": user.bio_msg,
        "profile_photo_id": user.profile_photo_id,
        "ubication": user.ubication,
        "is_followed": user.is_followed,
        "is_followed_back": user.is_followed_back,
        "blocked": user.blocked,
        "certified": user.certified,
    }
