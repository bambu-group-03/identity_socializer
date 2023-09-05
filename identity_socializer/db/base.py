from sqlalchemy.orm import DeclarativeBase

from identity_socializer.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
