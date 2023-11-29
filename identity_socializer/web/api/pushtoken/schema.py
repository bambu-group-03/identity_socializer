from pydantic import BaseModel, ConfigDict


class PushTokenEntry(BaseModel):
    """DTO for logger entry."""

    user_id: str
    pushtoken: str

    model_config = ConfigDict(from_attributes=True)
