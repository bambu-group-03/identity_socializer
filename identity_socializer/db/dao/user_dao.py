from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
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
        phone_number: Optional[str] = None,
        bio_msg: Optional[str] = None,
    ) -> None:

        """
        Add single user to session.

        It could contain only id and email.
        """
        user_model = UserModel(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            bio_msg=bio_msg,
            id=uid,
            email=email,
        )

        self.session.add(user_model)

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
