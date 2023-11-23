from fastapi import APIRouter, Depends

from identity_socializer.db.dao.logger_dao import LoggerDAO
from identity_socializer.db.models.logger_model import LogEvent
from identity_socializer.web.api.logger.schema import LoggerEntry

router = APIRouter()


@router.post("/loging_successful")
async def loging_successful(
    logger_entry: LoggerEntry,
    logger_dao: LoggerDAO = Depends(),
) -> None:
    """Log successful login."""
    event = LogEvent.LOGIN_SUCCESSFUL

    await logger_dao.create_logger_model(
        event=event.value,
        message=logger_entry.message,
        email=logger_entry.email,
    )


@router.post("/loging_error")
async def loging_error(
    logger_entry: LoggerEntry,
    logger_dao: LoggerDAO = Depends(),
) -> None:
    """Log failed login."""
    event = LogEvent.LOGIN_ERROR

    await logger_dao.create_logger_model(
        event=event.value,
        message=logger_entry.message,
        email=logger_entry.email,
    )


@router.post("/signup_successful")
async def signup_successful(
    logger_entry: LoggerEntry,
    logger_dao: LoggerDAO = Depends(),
) -> None:
    """Log successful signup."""
    event = LogEvent.SIGNUP_SUCCESSFUL

    await logger_dao.create_logger_model(
        event=event.value,
        message=logger_entry.message,
        email=logger_entry.email,
    )


@router.post("/signup_error")
async def signup_error(
    logger_entry: LoggerEntry,
    logger_dao: LoggerDAO = Depends(),
) -> None:
    """Log failed signup."""
    event = LogEvent.SIGNUP_ERROR

    await logger_dao.create_logger_model(
        event=event.value,
        message=logger_entry.message,
        email=logger_entry.email,
    )


@router.post("/logout_successful")
async def logout_successful(
    logger_entry: LoggerEntry,
    logger_dao: LoggerDAO = Depends(),
) -> None:
    """Log successful logout."""
    event = LogEvent.LOGOUT_SUCCESSFUL

    await logger_dao.create_logger_model(
        event=event.value,
        message=logger_entry.message,
        email=logger_entry.email,
    )
