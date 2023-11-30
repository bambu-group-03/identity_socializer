from typing import Dict, List, Optional

from fastapi import Depends
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from identity_socializer.db.dependencies import get_db_session
from identity_socializer.db.models.logger_model import LogEvent, LoggerModel
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

    async def get_all_logs(self, limit: int, offset: int) -> List[LoggerModel]:
        """Get all logs models with limit/offset pagination."""
        raw_logs = await self.session.execute(
            select(LoggerModel)
            .limit(limit)
            .offset(offset)
            .order_by(LoggerModel.created_at.desc()),
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

    async def get_sign_up_rates(self) -> Dict[str, int]:
        """Get sign up rates."""
        res_success = await self.session.execute(
            select(func.count(LoggerModel.id)).where(
                LoggerModel.event == LogEvent.SIGNUP_SUCCESSFUL.value,
            ),
        )

        res_error = await self.session.execute(
            select(func.count(LoggerModel.id)).where(
                LoggerModel.event == LogEvent.SIGNUP_ERROR.value,
            ),
        )

        res_complete_success = await self.session.execute(
            select(func.count(LoggerModel.id)).where(
                LoggerModel.event == LogEvent.COMPLETE_SIGNUP_SUCCESSFUL.value,
            ),
        )

        res_complete_error = await self.session.execute(
            select(func.count(LoggerModel.id)).where(
                LoggerModel.event == LogEvent.COMPLETE_SIGNUP_ERROR.value,
            ),
        )

        n_sign_up_successful = res_success.scalar() or 0
        n_sign_up_error = res_error.scalar() or 0
        n_complete_sign_up_successful = res_complete_success.scalar() or 0
        n_complete_sign_up_error = res_complete_error.scalar() or 0

        total_sign_ups = n_sign_up_successful + n_sign_up_error

        sign_up_successful_rate = (
            0 if total_sign_ups == 0 else (n_sign_up_successful / total_sign_ups) * 100
        )
        sign_up_error_rate = (
            0 if total_sign_ups == 0 else (n_sign_up_error / total_sign_ups) * 100
        )

        total_complete_sign_up = (
            n_complete_sign_up_successful + n_complete_sign_up_error
        )

        complete_sign_up_successful_rate = (
            0
            if total_complete_sign_up == 0
            else (n_complete_sign_up_successful / total_sign_ups) * 100
        )

        complete_sign_up_error_rate = (
            0
            if total_complete_sign_up == 0
            else (n_complete_sign_up_error / total_sign_ups) * 100
        )

        return {
            "total_sign_ups": int(total_sign_ups),
            "sign_up_successful": int(n_sign_up_successful),
            "sign_up_error": int(n_sign_up_error),
            "sign_up_successful_rate": int(sign_up_successful_rate),
            "sign_up_error_rate": int(sign_up_error_rate),
            "total_complete_sign_up": int(total_complete_sign_up),
            "complete_sign_up_successful": int(n_complete_sign_up_successful),
            "complete_sign_up_error": int(n_complete_sign_up_error),
            "complete_sign_up_successful_rate": int(complete_sign_up_successful_rate),
            "complete_sign_up_error_rate": int(complete_sign_up_error_rate),
        }

    async def get_log_in_rates(self) -> Dict[str, int]:
        """Get log in rates."""
        res_success = await self.session.execute(
            select(func.count(LoggerModel.id)).where(
                LoggerModel.event == LogEvent.LOGIN_SUCCESSFUL.value,
            ),
        )

        res_error = await self.session.execute(
            select(func.count(LoggerModel.id)).where(
                LoggerModel.event == LogEvent.LOGIN_ERROR.value,
            ),
        )

        n_log_in_successful = res_success.scalar() or 0
        n_log_in_error = res_error.scalar() or 0

        total_log_ins = n_log_in_successful + n_log_in_error

        log_in_successful_rate = (
            0 if total_log_ins == 0 else (n_log_in_successful / total_log_ins) * 100
        )
        log_in_error_rate = (
            0 if total_log_ins == 0 else (n_log_in_error / total_log_ins) * 100
        )

        return {
            "total_log_ins": int(total_log_ins),
            "log_in_successful": int(n_log_in_successful),
            "log_in_error": int(n_log_in_error),
            "log_in_successful_rate": int(log_in_successful_rate),
            "log_in_error_rate": int(log_in_error_rate),
        }
