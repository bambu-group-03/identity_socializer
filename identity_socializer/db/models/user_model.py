from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from identity_socializer.db.base import Base


class UserModel(Base):
    """Model for User."""

    __tablename__ = "users"

    length = 200

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length))
    email: Mapped[str] = mapped_column(String(length))
