from typing import List, Optional

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from identity_socializer.db.dependencies import get_db_session
from identity_socializer.db.models.logger_model import LoggerModel
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
