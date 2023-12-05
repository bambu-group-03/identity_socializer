import datetime
import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime, String, Uuid

from identity_socializer.db.base import Base


class CertifiedRequestModel(Base):
    """Model for CertifiedRequest."""

    __tablename__ = "certified_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        default=uuid.uuid4,
        primary_key=True,
    )
    user_id: Mapped[str] = mapped_column(String())
    dni: Mapped[str] = mapped_column(String())
    img1_url: Mapped[str] = mapped_column(String())
    img2_url: Mapped[str] = mapped_column(String())
    status: Mapped[str] = mapped_column(String())

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
    )
