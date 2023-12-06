import datetime
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from identity_socializer.db.dependencies import get_db_session
from identity_socializer.db.models.user_model import UserModel


class UserDAO:
    """Class for accessing users table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user_model(
        self,
        uid: str,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        phone_number: Optional[str] = None,
        bio_msg: Optional[str] = None,
        ubication: Optional[str] = None,
    ) -> None:

        """
        Add single user to session.

        It could contain only id and email.
        """
        user_model = UserModel(
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
            bio_msg=bio_msg,
            id=uid,
            email=email,
            ubication=ubication,
        )

        self.session.add(user_model)

    async def update_user_model(
        self,
        uid: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        phone_number: Optional[str] = None,
        bio_msg: Optional[str] = None,
        profile_photo_id: Optional[str] = None,
        ubication: Optional[str] = None,
        interests: Optional[list] = None,
    ) -> None:

        """Update single user to session."""
        stmt = (
            update(UserModel)
            .where(UserModel.id == uid)
            .values(
                first_name=first_name,
                last_name=last_name,
                username=username,
                phone_number=phone_number,
                bio_msg=bio_msg,
                profile_photo_id=profile_photo_id,
                ubication=ubication,
                interests=interests,
            )
        )

        await self.session.execute(stmt)

    async def block_user(
        self,
        user_id: str,
    ) -> None:

        """Block user by id."""
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(
                blocked=True,
            )
        )

        await self.session.execute(stmt)

    async def unblock_user(
        self,
        user_id: str,
    ) -> None:

        """Unblock user by id."""
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(
                blocked=False,
            )
        )

        await self.session.execute(stmt)

    async def get_all_users(self, limit: int, offset: int) -> List[UserModel]:
        """
        Get all users models with limit/offset pagination.

        :param limit: limit of users.
        :param offset: offset of users.
        :return: stream of users.
        """
        raw_users = await self.session.execute(
            select(UserModel).limit(limit).offset(offset),
        )

        return list(raw_users.scalars().fetchall())

    async def filter(
        self,
        first_name: Optional[str] = None,
    ) -> List[UserModel]:
        """
        Get specific user model.

        :param name: name of user instance.
        :return: users models.
        """
        query = select(UserModel)
        if first_name:
            query = query.where(UserModel.first_name == first_name)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_user_by_id(self, user_id: str) -> Optional[UserModel]:
        """Get specific user model."""
        query = select(UserModel).where(UserModel.id == user_id)
        rows = await self.session.execute(query)
        return rows.scalars().first()

    async def filter_user(
        self,
        username: str,
    ) -> List[UserModel]:
        """Get list of filtered users by username and/or id."""
        query = select(UserModel)
        query = query.filter(UserModel.username.ilike(f"%{username}%"))

        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_user_by_username(self, username: str) -> Optional[UserModel]:
        """Get specific user model."""
        query = select(UserModel)
        query = query.filter(func.lower(UserModel.username) == func.lower(username))

        rows = await self.session.execute(query)
        return rows.scalars().first()

    async def get_username_by_id(self, user_id: str) -> Optional[str]:
        """Get specific user model."""
        query = select(UserModel.username).where(UserModel.id == user_id)
        rows = await self.session.execute(query)
        return rows.scalars().first()

    async def count_new_users_between_dates(
        self,
        start_date_str: str,
        end_date_str: str,
    ) -> int:
        """Get new users between dates."""
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

        query = select(func.count(UserModel.id))
        query = query.where(UserModel.created_at >= start_date)
        query = query.where(UserModel.created_at <= end_date)

        rows = await self.session.execute(query)

        return rows.scalar() or 0

    async def update_certified(
        self,
        user_id: str,
        certified: bool,
    ) -> None:
        """Update certified."""
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(
                certified=certified,
            )
        )

        await self.session.execute(stmt)
