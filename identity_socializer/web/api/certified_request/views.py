from typing import Any

from fastapi import APIRouter, Depends

from identity_socializer.db.dao.certified_request_dao import (
    CertifiedRequestDAO,
    StatusRequest,
)
from identity_socializer.db.dao.user_dao import UserDAO
from identity_socializer.web.api.certified_request.schema import CertifiedRequestDTO

router = APIRouter()


@router.post("/register", response_model=None)
async def create_certified_request(
    body: CertifiedRequestDTO,
    dao: CertifiedRequestDAO = Depends(),
    dao_user: UserDAO = Depends(),
) -> None:
    # Create certified request
    """Register certified request from user."""
    await dao.create_certified_request(
        user_id=body.user_id,
        dni=body.dni,
        img1_url=body.img1_url,
        img2_url=body.img2_url,
    )

    # Update user certified identity
    await dao_user.update_certified(user_id=body.user_id, certified=False)


@router.get("/get_all_certified_requests", response_model=None)
async def get_all_certified_requests(
    limit: int = 10,
    offset: int = 0,
    cq_dao: CertifiedRequestDAO = Depends(),
    user_dao: UserDAO = Depends(),
) -> Any:
    """Get all certified requests."""
    completed_cqs = []

    certifieds = await cq_dao.get_all_certified_requests(limit=limit, offset=offset)

    for certified in certifieds:

        user = await user_dao.get_user_by_id(certified.user_id)

        username = user.username if user else "unknown"
        email = user.email if user else "unknown"

        completed_cq = {
            "id": certified.id,
            "user_id": certified.user_id,
            "dni": certified.dni,
            "img1_url": certified.img1_url,
            "img2_url": certified.img2_url,
            "status": certified.status,
            "created_at": certified.created_at,
            "username": username,
            "email": email,
        }
        completed_cqs.append(completed_cq)

    return completed_cqs


@router.delete("/delete/{certified_request_id}", response_model=None)
async def delete_certified_request(
    certified_request_id: str,
    dao: CertifiedRequestDAO = Depends(),
    dao_user: UserDAO = Depends(),
) -> None:
    """Delete certified request."""
    # Check if certified request exists
    certified_request = await dao.get_certified_request(certified_request_id)

    if not certified_request:
        return

    # Delete certified request
    await dao.delete_certified_request(certified_request.id)

    # Update user certified identity
    await dao_user.update_certified(user_id=certified_request.user_id, certified=False)


@router.put("/approve/{certified_request_id}", response_model=None)
async def approve_certified_request(
    certified_request_id: str,
    dao: CertifiedRequestDAO = Depends(),
    dao_user: UserDAO = Depends(),
) -> None:
    """Approve certified request."""
    # Check if certified request exists
    certified_request = await dao.get_certified_request(certified_request_id)

    if not certified_request:
        return

    # Update certified request status
    new_status = StatusRequest.APPROVED.value
    await dao.update_status(certified_request_id, new_status)

    # Update user certified identity
    await dao_user.update_certified(user_id=certified_request.user_id, certified=True)


@router.put("/reject/{certified_request_id}", response_model=None)
async def reject_certified_request(
    certified_request_id: str,
    dao: CertifiedRequestDAO = Depends(),
) -> None:
    """Reject certified request."""
    # Check if certified request exists
    certified_request = await dao.get_certified_request(certified_request_id)

    if not certified_request:
        return

    # Update certified request status
    new_status = StatusRequest.REJECTED.value
    await dao.update_status(certified_request_id, new_status)
