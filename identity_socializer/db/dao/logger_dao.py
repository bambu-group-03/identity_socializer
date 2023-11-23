from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from identity_socializer.db.dependencies import get_db_session
from identity_socializer.db.models.logger_model import LoggerModel


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
