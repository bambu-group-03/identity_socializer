from typing import Any

import httpx

from identity_socializer.db.dao.push_token_dao import PushTokenDAO


class PushNotifications:
    """Class for sending push notifications."""

    def send(self, notification: Any) -> None:
        """Send push notification to user."""
        res = httpx.post(
            "https://exp.host/--/api/v2/push/send",
            json=notification,
        )

        print(f"Expo response status code: {res.status_code}")

    async def new_follower(
        self,
        user_id: str,
        push_token_dao: PushTokenDAO,
    ) -> None:
        """Send push notification for new follower."""
        push_tokens = await push_token_dao.get_push_tokens_by_user(user_id)

        for push_token in push_tokens:

            notification = {
                "to": push_token,
                "sound": "default",
                "title": "New follower",
                "body": "You have a new follower!",
                "data": {"extra": "extra_data"},
            }

            self.send(notification)
