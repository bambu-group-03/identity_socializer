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

    async def get_user_rates(self) -> Dict[str, str]:
        """Get blocked rate."""
        res_users = await self.session.execute(select(func.count(UserModel.id)))

        res_blocked = await self.session.execute(
            select(func.count(UserModel.id)).where(UserModel.blocked == True),
        )

        n_users = res_users.scalar() or 0
        n_blocked_users = res_blocked.scalar() or 0

        blocked_user_rate = 0 if n_users == 0 else (n_blocked_users / n_users) * 100
        non_blocked_user_rate = 100 - blocked_user_rate

        return {
            "total_users": str(n_users),
            "blocked_users": str(n_blocked_users),
            "non_blocked_users": str(round(n_users - n_blocked_users, 1)),
            "blocked_users_rate": str(round(blocked_user_rate, 1)),
            "non_blocked_users_rate": str(round(non_blocked_user_rate, 1)),
        }

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

    async def get_sign_up_rates(self) -> Dict[str, str]:
        """Get sign up rates."""
        res_success = await self.session.execute(
            select(func.count(LoggerModel.id)).where(
                LoggerModel.event == LogEvent.SIGNUP_SUCCESSFUL.value,
            ),
        )

        res_google = await self.session.execute(
            select(func.count(LoggerModel.id)).where(
                LoggerModel.event == LogEvent.SIGNUP_GOOGLE.value,
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
        n_sign_up_google = res_google.scalar() or 0

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
            else (n_complete_sign_up_successful / total_complete_sign_up) * 100
        )

        complete_sign_up_error_rate = (
            0
            if total_complete_sign_up == 0
            else (n_complete_sign_up_error / total_complete_sign_up) * 100
        )

        return {
            "total_sign_ups": str(total_sign_ups),
            "sign_up_successful": str(n_sign_up_successful),
            "sign_up_google": str(n_sign_up_google),
            "sign_up_error": str(n_sign_up_error),
            "sign_up_successful_rate": str(round(sign_up_successful_rate, 1)),
            "sign_up_error_rate": str(round(sign_up_error_rate, 1)),
            "total_complete_sign_up": str(total_complete_sign_up),
            "complete_sign_up_successful": str(n_complete_sign_up_successful),
            "complete_sign_up_error": str(n_complete_sign_up_error),
            "complete_sign_up_successful_rate": str(
                round(
                    complete_sign_up_successful_rate,
                    1,
                ),
            ),
            "complete_sign_up_error_rate": str(round(complete_sign_up_error_rate, 1)),
        }

    async def get_log_in_rates(self) -> Dict[str, str]:
        """Get log in rates."""
        res_success = await self.session.execute(
            select(func.count(LoggerModel.id)).where(
                LoggerModel.event == LogEvent.LOGIN_SUCCESSFUL.value,
            ),
        )

        res_google = await self.session.execute(
            select(func.count(LoggerModel.id)).where(
                LoggerModel.event == LogEvent.LOGIN_GOOGLE.value,
            ),
        )

        res_error = await self.session.execute(
            select(func.count(LoggerModel.id)).where(
                LoggerModel.event == LogEvent.LOGIN_ERROR.value,
            ),
        )

        n_log_in_successful = res_success.scalar() or 0
        n_log_in_google = res_google.scalar() or 0
        n_log_in_error = res_error.scalar() or 0

        total_log_ins = n_log_in_successful + n_log_in_error

        log_in_successful_rate = (
            0 if total_log_ins == 0 else (n_log_in_successful / total_log_ins) * 100
        )
        log_in_error_rate = (
            0 if total_log_ins == 0 else (n_log_in_error / total_log_ins) * 100
        )

        return {
            "total_log_ins": str(total_log_ins),
            "log_in_successful": str(n_log_in_successful),
            "log_in_google": str(n_log_in_google),
            "log_in_error": str(n_log_in_error),
            "log_in_successful_rate": str(round(log_in_successful_rate, 1)),
            "log_in_error_rate": str(round(log_in_error_rate, 1)),
        }
