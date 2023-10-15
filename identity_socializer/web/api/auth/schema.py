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
    email: str
    first_name: str | None
    last_name: str | None
    phone_number: str | None
    bio_msg: str | None
    model_config = ConfigDict(from_attributes=True)


class SimpleUserModelDTO(BaseModel):
    """Message model for user register."""

    id: str
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)
