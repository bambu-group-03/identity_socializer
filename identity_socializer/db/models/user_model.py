import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Boolean, DateTime, String

from identity_socializer.db.base import Base


class UserModel(Base):
    """Model for User."""

    __tablename__ = "users"

    length = 200

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(length))
    first_name: Mapped[str] = mapped_column(String(length), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length), nullable=True)
    username: Mapped[str] = mapped_column(String(length), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(length), nullable=True)
    bio_msg: Mapped[str] = mapped_column(String(length), nullable=True)
    profile_photo_id: Mapped[str] = mapped_column(String(length), nullable=True)
    blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow(),
        nullable=False,
    )
