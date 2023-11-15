from pydantic import BaseModel, ConfigDict


class MessageDTO(BaseModel):
    """DTO for chat message."""

    from_id: str
    to_id: str
    content: str

    model_config = ConfigDict(from_attributes=True)
