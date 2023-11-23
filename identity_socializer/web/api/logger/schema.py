from typing import Optional

from pydantic import BaseModel, ConfigDict


class LoggerEntry(BaseModel):
    """DTO for logger entry."""

    message: Optional[str]
    email: Optional[str]

    model_config = ConfigDict(from_attributes=True)
