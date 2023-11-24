from pydantic import BaseModel, ConfigDict


class NotificationDTO(BaseModel):
    """DTO for chat message."""

    user_id: str
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)


class NotificationSchema(BaseModel):
    """DTO for chat."""

    id: str
    user_id: str
    title: str
    content: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)
