from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from identity_socializer.db.dependencies import get_db_session
from identity_socializer.db.models.relationship_model import RelationshipModel


class RelationshipDAO:
    """Class for accessing relationships table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_relationship_model(
        self,
        follower_id: str,
        following_id: str,
    ) -> None:
        """Add single relationship to session."""
        relationship_model = RelationshipModel(
            follower_id=follower_id,
            following_id=following_id,
        )

        self.session.add(relationship_model)

    async def get_following_by_id(self, user_id: str) -> List[RelationshipModel]:
        """Get following users by id."""
        query = select(RelationshipModel).where(
            RelationshipModel.follower_id == user_id,
        )
        rows = await self.session.execute(query)

        return list(rows.scalars().fetchall())

    async def get_followers_by_id(self, user_id: str) -> List[RelationshipModel]:
        """Get followers users by id."""
        query = select(RelationshipModel).where(
            RelationshipModel.following_id == user_id,
        )
        rows = await self.session.execute(query)

        return list(rows.scalars().fetchall())
