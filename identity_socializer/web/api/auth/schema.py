from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class UserModelDTO(BaseModel):
    """Message model for user register."""

    id: str
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    phone_number: Optional[str]
    bio_msg: Optional[str]
    profile_photo_id: Optional[str]
    ubication: Optional[str]
    interests: Optional[List[str]]
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


class AppUserModel(BaseModel):
    """Message model for user register."""

    id: str
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    phone_number: Optional[str]
    bio_msg: Optional[str]
    profile_photo_id: Optional[str]
    ubication: Optional[str]
    is_followed: Optional[bool]
    is_followed_back: Optional[bool] = False
    blocked: bool = False
    certified: bool = False
    interests: Optional[List[str]]
    model_config = ConfigDict(from_attributes=True)
