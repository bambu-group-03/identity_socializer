from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from identity_socializer.db.dependencies import get_db_session
from identity_socializer.db.models.admin_model import AdminModel


class AdminDAO:
    """Class for accessing admins table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_admin_model(
        self,
        admin_id: str,
        email: str,
    ) -> None:
        """Add single admin to session."""
        admin_model = AdminModel(
            id=admin_id,
            email=email,
        )

        self.session.add(admin_model)

    async def get_all_admins(self, limit: int, offset: int) -> List[AdminModel]:
        """
        Get all admins models with limit/offset pagination.

        :param limit: limit of admins.
        :param offset: offset of admins.
        :return: stream of admins.
        """
        raw_admins = await self.session.execute(
            select(AdminModel).limit(limit).offset(offset),
        )

        return list(raw_admins.scalars().fetchall())
