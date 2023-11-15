from typing import Optional

from pydantic import BaseModel, ConfigDict


class SecurityToken(BaseModel):
    """Firebase-generated token."""

    token: str


class Success(BaseModel):
    """Success message."""

    msg: str


class UserModelDTO(BaseModel):
    """Message model for user register."""

    id: str
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    phone_number: Optional[str]
    bio_msg: Optional[str]
    profile_photo_url: Optional[str]
    ubication: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class SimpleUserModelDTO(BaseModel):
    """Message model for user register."""

    id: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class AdminDTO(BaseModel):
    """Message model for admin register."""

    id: str
    email: str
    model_config = ConfigDict(from_attributes=True)
