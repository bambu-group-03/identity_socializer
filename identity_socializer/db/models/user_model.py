from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from identity_socializer.db.base import Base


class UserModel(Base):
    """Model for User."""

    __tablename__ = "users"

    length = 200

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(length))
    first_name: Mapped[str] = mapped_column(String(length))
    last_name: Mapped[str] = mapped_column(String(length))
    phone_number: Mapped[str] = mapped_column(String(length))
    bio_msg: Mapped[str] = mapped_column(String(length))
    profile_photo_id: Mapped[str] = mapped_column(String(length))
