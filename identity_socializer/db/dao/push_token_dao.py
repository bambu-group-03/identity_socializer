from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from identity_socializer.db.dependencies import get_db_session
from identity_socializer.db.models.push_token_model import PushTokenModel


class PushTokenDAO:
    """Class for accessing users table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_push_token(
        self,
        user_id: str,
        pushtoken: str,
    ) -> None:
        """Add single push token to session."""
        try:

            push_token = PushTokenModel(
                user_id=user_id,
                pushtoken=pushtoken,
            )

            self.session.add(push_token)

        except Exception:
            print("Push token already exists")

    async def get_push_tokens_by_user(self, user_id: str) -> List[str]:
        """Get list push tokens from user."""
        pushtokens = await self.session.execute(
            select(PushTokenModel.pushtoken).where(PushTokenModel.user_id == user_id),
        )

        return list(pushtokens.scalars().fetchall())
