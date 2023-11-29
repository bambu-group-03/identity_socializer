from typing import List, Optional

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from identity_socializer.db.dependencies import get_db_session
from identity_socializer.db.models.relationship_model import RelationshipModel
from identity_socializer.db.models.user_model import UserModel


class RelationshipDAO:
    """Class for accessing relationships table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_relationship_model(
        self,
        follower_id: str,
        following_id: str,
    ) -> Optional[RelationshipModel]:
        """Add single relationship to session."""
        try:
            relationship_model = RelationshipModel(
                follower_id=follower_id,
                following_id=following_id,
            )

            self.session.add(relationship_model)
            await self.session.flush()

            return relationship_model
        except Exception:
            return None

    async def delete_relationship_model(
        self,
        follower_id: str,
        following_id: str,
    ) -> None:
        """Delete single relationship from session."""
        query = delete(RelationshipModel).where(
            RelationshipModel.follower_id == follower_id,
            RelationshipModel.following_id == following_id,
        )
        await self.session.execute(query)

    async def get_following_by_id(self, user_id: str) -> List[UserModel]:
        """Get following of user_id."""
        query = (
            select(UserModel)
            .distinct()
            .join(
                RelationshipModel.following,
            )
            .where(
                RelationshipModel.follower_id == user_id,
            )
        )
        rows = await self.session.execute(query)

        return list(rows.scalars().fetchall())

    async def get_followers_by_id(self, user_id: str) -> List[UserModel]:
        """Get followers of user_id."""
        query = (
            select(UserModel)
            .distinct()
            .join(
                RelationshipModel.follower,
            )
            .where(
                RelationshipModel.following_id == user_id,
            )
        )
        rows = await self.session.execute(query)

        return list(rows.scalars().fetchall())

    async def count_following_by_user_id(self, user_id: str) -> int:
        """Get number of following of user_id."""
        following = await self.get_following_by_id(user_id)

        return len(following)

    async def count_followers_by_user_id(self, user_id: str) -> int:
        """Get number of followers of user_id."""
        followers = await self.get_followers_by_id(user_id)

        return len(followers)

    async def is_followed_by_user(self, current_user_id: str, user_id: str) -> bool:
        """Returns true if user_id is followed by current_user_id."""
        query = select(RelationshipModel)
        query = query.where(RelationshipModel.follower_id == current_user_id).where(
            RelationshipModel.following_id == user_id,
        )

        rows = await self.session.execute(query)
        my_list = list(rows.scalars().fetchall())

        return bool(my_list)

    async def is_mutuals(self, user1: str, user2: str) -> bool:
        """
        True if both users follow each other.

        Does not consider if both users are the same.
        """
        followed = await self.is_followed_by_user(user1, user2)
        follower = await self.is_followed_by_user(user2, user1)
        return followed and follower
