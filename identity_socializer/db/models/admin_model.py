import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime, String

from identity_socializer.db.base import Base


class AdminModel(Base):
    """Model for Admin."""

    __tablename__ = "admins"

    length = 200

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(length))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
    )
