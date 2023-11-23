import datetime
import uuid
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime, String, Uuid

from identity_socializer.db.base import Base


class LogEvent(Enum):
    """Enum for logger events."""

    LOGIN_SUCCESSFUL = "LOGIN_SUCCESSFUL"
    LOGIN_ERROR = "LOGIN_ERROR"
    SIGNUP_SUCCESSFUL = "SIGNUP_SUCCESSFUL"
    SIGNUP_ERROR = "SIGNUP_ERROR"
    COMPLETE_SIGNUP_SUCCESSFUL = "COMPLETE_SIGNUP_SUCCESSFUL"
    LOGOUT_SUCCESSFUL = "LOGOUT_SUCCESSFUL"


class LoggerModel(Base):
    """Model for Logger."""

    __tablename__ = "logger"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        default=uuid.uuid4,
        primary_key=True,
    )
    event: Mapped[str] = mapped_column(String(), nullable=False)
    message: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String())
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False,
    )
