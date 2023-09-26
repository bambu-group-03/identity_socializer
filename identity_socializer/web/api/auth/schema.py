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
    name: str
    model_config = ConfigDict(from_attributes=True)
