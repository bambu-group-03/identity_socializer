import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime, String

from identity_socializer.db.base import Base


class RelationshipModel(Base):
    """Model for Relationship."""

    __tablename__ = "relationships"

    length = 200

    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[str] = mapped_column(String(length), ForeignKey("users.id"))
    following_id: Mapped[str] = mapped_column(String(length), ForeignKey("users.id"))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow(),
    )

    follower = relationship("UserModel", foreign_keys=[follower_id])
    following = relationship("UserModel", foreign_keys=[following_id])
