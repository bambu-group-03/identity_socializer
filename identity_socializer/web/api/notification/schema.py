from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class NotificationDTO(BaseModel):
    """DTO for notification message."""

    from_id: str
    to_id: str
    snap: Any

    model_config = ConfigDict(from_attributes=True)


class TrendingNotificationDTO(BaseModel):
    """DTO for trending notification message."""

    topic: str
    snap: Any

    model_config = ConfigDict(from_attributes=True)


class NotificationSchema(BaseModel):
    """DTO for chat."""

    id: str
    user_id: str
    title: str
    content: str
    notification_type: Optional[str]
    redirect_id: Optional[str]
    created_at: str

    model_config = ConfigDict(from_attributes=True)
