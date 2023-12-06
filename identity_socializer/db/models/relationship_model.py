import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime, String, Uuid

from identity_socializer.db.base import Base


class RelationshipModel(Base):
    """Model for Relationship."""

    __tablename__ = "relationships"

    length = 200

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        default=uuid.uuid4,
        primary_key=True,
    )
    follower_id: Mapped[str] = mapped_column(String(length), ForeignKey("users.id"))
    following_id: Mapped[str] = mapped_column(String(length), ForeignKey("users.id"))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
    )

    follower = relationship("UserModel", foreign_keys=[follower_id])
    following = relationship("UserModel", foreign_keys=[following_id])


class InterestModel(Base):
    """Model for Interests."""

    __tablename__ = "interests"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # Relationship back to UserModel
    users = relationship(
        "UserModel",
        secondary="user_interests",
        back_populates="interests",
    )
