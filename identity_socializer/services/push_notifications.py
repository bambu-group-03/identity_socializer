from typing import Any

import httpx

from identity_socializer.db.collections.chats import get_chats_by_user_id
from identity_socializer.db.collections.notifications import create_notification
from identity_socializer.db.dao.push_token_dao import PushTokenDAO
from identity_socializer.db.dao.relationship_dao import RelationshipDAO
from identity_socializer.db.dao.user_dao import UserDAO
from identity_socializer.web.api.auth.views import get_user_model


class PushNotifications:
    """Class for sending push notifications."""

    def send(self, notification: Any) -> None:
        """Send push notification to user."""
        try:
            httpx.post(
                "https://exp.host/--/api/v2/push/send",
                json=notification,
            )
        except Exception as e:
            print(e)

    def save_notification(self, user_id: str, title: str, content: str) -> None:
        """Save notification to database."""
        create_notification(
            user_id=user_id,
            title=title,
            content=content,
        )

    async def new_like(
        self,
        from_id: str,
        to_id: str,
        snap_id: str,
        user_dao: UserDAO,
        push_token_dao: PushTokenDAO,
    ) -> None:
        """Send push notification for new like."""
        snap = _get_snap(snap_id, to_id)

        if snap is None:
            return

        username = await user_dao.get_username_by_id(from_id) or "unknown"

        # Create and save notification to database
        title = "Your snap have a new like!"
        body = f"@{username} liked your snap!"

        self.save_notification(to_id, title, body)

        # Send push notification to user
        push_tokens = await push_token_dao.get_push_tokens_by_user(to_id)
        for push_token in push_tokens:

            data = {
                "screen": "LikeNotification",
                "params": snap,
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

        self.save_notification(to_id, title, body)

        # Send push notification to user
        push_tokens = await push_token_dao.get_push_tokens_by_user(to_id)
        for push_token in push_tokens:

            data = {
                "screen": "NewFollowerNotification",
                "params": user,
            }

            notification = _create_push_notification(push_token, title, body, data)

            self.send(notification)

    async def new_mention(
        self,
        from_id: str,
        to_id: str,
        snap_id: str,
        user_dao: UserDAO,
        push_token_dao: PushTokenDAO,
    ) -> None:
        """Send push notification for new mention."""
        snap = _get_snap(snap_id, to_id)

        if snap is None:
            return

        username = await user_dao.get_username_by_id(from_id) or "unknown"

        # Create and save notification to database
        title = "You have a new mention!"
        body = f"@{username} mentioned you!"

        self.save_notification(to_id, title, body)

        # Send push notification to user
        push_tokens = await push_token_dao.get_push_tokens_by_user(to_id)
        for push_token in push_tokens:

            data = {
                "screen": "NewMentionNotification",
                "params": snap,
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

        chat = get_chats_by_user_id(chat_to_id)

        if chat is None:
            return

        # Create and save notification to database
        title = "You have a new message!"
        body = f"@{user.username} sent you a message!"

        self.save_notification(to_id, title, body)

        # Send push notification to user
        push_tokens = await push_token_dao.get_push_tokens_by_user(to_id)
        for push_token in push_tokens:

            data = {
                "screen": "NewMessageNotification",
                "params": {chat, user},
            }

            notification = _create_push_notification(push_token, title, body, data)

            self.send(notification)


def _create_push_notification(push_token: str, title: str, body: str, data: Any) -> Any:
    return {
        "to": push_token,
        "sound": "default",
        "title": title,
        "body": body,
        "data": data,
    }


def _get_snap(snap_id: str, user_id: str) -> Any:
    """Get snap from content discovery."""
    url = "https://api-content-discovery-luiscusihuaman.cloud.okteto.net"

    res = httpx.get(
        f"{url}/api/feed/snap/{snap_id}?user_id={user_id}",
    )

    if res.status_code != 200:
        return None
    return res.json()
