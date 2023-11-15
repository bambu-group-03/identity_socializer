from pydantic import BaseModel, ConfigDict


class MessageDTO(BaseModel):
    """DTO for chat message."""

    from_id: str
    to_id: str
    content: str

    model_config = ConfigDict(from_attributes=True)


class MessageSchema(BaseModel):
    """DTO for chat."""

    msg_id: str
    from_id: str
    to_id: str
    content: str
    chat_id: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class ChatDTO(BaseModel):
    """DTO for chat."""

    chat_id: str
    owner_id: str
    other_id: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)
