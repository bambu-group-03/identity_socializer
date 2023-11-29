import datetime
import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime, String, Uuid

from identity_socializer.db.base import Base


class PushTokenModel(Base):
    """Model for PushToken."""

    __tablename__ = "pushtokens"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        default=uuid.uuid4,
        primary_key=True,
    )
    user_id: Mapped[str] = mapped_column(String())
    pushtoken: Mapped[str] = mapped_column(String())

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
    )
