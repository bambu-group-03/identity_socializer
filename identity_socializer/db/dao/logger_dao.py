from typing import Dict, List, Optional

from fastapi import Depends
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from identity_socializer.db.dependencies import get_db_session
from identity_socializer.db.models.logger_model import LoggerModel
from identity_socializer.db.models.user_model import UserModel
from identity_socializer.db.utils import is_valid_uuid


class LoggerDAO:
    """Class for accessing logger table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_logger_model(
        self,
        event: str,
        message: Optional[str] = None,
        email: Optional[str] = None,
    ) -> None:
        """Add single logger to session."""
        logger_entry = LoggerModel(
            event=event,
            message=message,
            email=email,
        )

        self.session.add(logger_entry)

    async def get_all_logs(self) -> List[LoggerModel]:
        """Get all logs."""
        raw_logs = await self.session.execute(
            select(LoggerModel),
        )

        return list(raw_logs.scalars().fetchall())

    async def delete_log(self, log_id: str) -> None:
        """Delete log by id."""
        if not is_valid_uuid(log_id):
            return

        query = delete(LoggerModel).where(LoggerModel.id == log_id)
        await self.session.execute(query)


class MetricDAO:
    """Class for accessing metrics."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_blocked_rate(self) -> int:
        """Get blocked rate."""
        # count all users
        users = await self.session.execute(select(UserModel))
        n_users = len(list(users.scalars().fetchall()))

        if n_users == 0:
            return 0

        # count all blocked users
        count_blocked_users = await self.session.execute(
            select(UserModel).where(UserModel.blocked == True),
        )
        n_blocked_users = len(list(count_blocked_users.scalars().fetchall()))

        if n_blocked_users == 0:
            return 0

        return int((n_blocked_users / n_users) * 100)

    async def get_ubication_count(self) -> Dict[str, str]:
        """Get ubication count."""
        res = {}

        query = select(UserModel.ubication, func.count(UserModel.id))
        query = query.group_by(UserModel.ubication)
        query = query.order_by(func.count(UserModel.id).desc())

        statistics = await self.session.execute(query)

        for (ubication, count) in statistics:
            res[ubication] = count

        return res
