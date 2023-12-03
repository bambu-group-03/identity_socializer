import uuid
from enum import Enum
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from identity_socializer.db.dependencies import get_db_session
from identity_socializer.db.models.certified_request_model import CertifiedRequestModel


class StatusRequest(Enum):
    """Enum for status requests."""

    APPROVED = "Approved"
    REJECTED = "Rejected"
    PENDING = "Pending"


class CertifiedRequestDAO:
    """Class for accessing certified requests table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_certified_request(
        self,
        user_id: str,
        dni: Optional[str],
        img1_url: Optional[str],
        img2_url: Optional[str],
    ) -> None:
        """Add single certified request to session."""
        query = CertifiedRequestModel(
            user_id=user_id,
            dni=dni,
            img1_url=img1_url,
            img2_url=img2_url,
            status=StatusRequest.PENDING.value,
        )
        self.session.add(query)

    async def delete_certified_request(
        self,
        certified_request_id: uuid.UUID,
    ) -> None:
        """Delete single certified request from session."""
        query = delete(CertifiedRequestModel).where(
            CertifiedRequestModel.id == certified_request_id,
        )
        await self.session.execute(query)

    async def get_all_certified_requests(
        self,
        limit: int,
        offset: int,
    ) -> List[CertifiedRequestModel]:
        """Get all certified request."""
        query = select(CertifiedRequestModel).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return list(result.scalars().fetchall())

    async def update_status(
        self,
        certified_request_id: str,
        status: str,
    ) -> None:
        """Update status certified request."""
        query = (
            update(CertifiedRequestModel)
            .where(
                CertifiedRequestModel.id == certified_request_id,
            )
            .where(CertifiedRequestModel.status == StatusRequest.PENDING.value)
            .values(
                status=status,
            )
        )
        await self.session.execute(query)

    async def get_certified_request(
        self,
        certified_request_id: str,
    ) -> Optional[CertifiedRequestModel]:
        """Get single certified request."""
        query = select(CertifiedRequestModel).where(
            CertifiedRequestModel.id == certified_request_id,
        )
        result = await self.session.execute(query)
        return result.scalars().first()
