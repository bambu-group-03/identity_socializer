from typing import Optional

from pydantic import BaseModel, ConfigDict


class CertifiedRequestDTO(BaseModel):
    """DTO for certified request entry."""

    user_id: str
    dni: Optional[str]
    img1_url: Optional[str]
    img2_url: Optional[str]

    model_config = ConfigDict(from_attributes=True)
