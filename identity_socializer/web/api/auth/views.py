from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import auth

from identity_socializer.db.dao.admin_dao import AdminDAO
from identity_socializer.db.dao.user_dao import UserDAO
from identity_socializer.db.models.admin_model import AdminModel
from identity_socializer.db.models.user_model import UserModel
from identity_socializer.web.api.auth.schema import (
    AdminDTO,
    SecurityToken,
    SimpleUserModelDTO,
    Success,
    UserModelDTO,
)

router = APIRouter()


@router.post("/signup", response_model=Success)
async def signup(
    incoming_message: SecurityToken,
) -> Success:
    """
    Sign up a user.

    :param incoming_message: Incoming message.
    :raises HTTPException: If something goes wrong.
    :return: Success message.
    """
    ret = Success(msg="Success")

    # todo: explorar cada caso de verify_id_token
    try:
        auth.verify_id_token(incoming_message.token)
        return ret
    except Exception as error:
        code = 500
        raise HTTPException(status_code=code, detail=str(error))


@router.post("/register", response_model=None)
async def register(
    simple_user: SimpleUserModelDTO,
    user_dao: UserDAO = Depends(),
) -> None:
    """Register a user with minimal information."""
    await user_dao.create_user_model(
        uid=simple_user.id,
        email=simple_user.email,
    )


@router.put("/update_user", response_model=None)
async def update_user(
    user: UserModelDTO,
    user_dao: UserDAO = Depends(),
) -> None:
    """Update a user."""
    await user_dao.update_user_model(
        uid=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone_number=user.phone_number,
        bio_msg=user.bio_msg,
        profile_photo_id=user.profile_photo_id,
        ubication=user.ubication,
    )


@router.put("/block_user/{user_id}")
async def block_user(
    user_id: str,
    user_dao: UserDAO = Depends(),
) -> None:
    """Block a single user."""
    await user_dao.block_user(user_id)


@router.put("/unblock_user/{user_id}")
async def unblock_user(
    user_id: str,
    user_dao: UserDAO = Depends(),
) -> None:
    """Unblock a single user."""
    await user_dao.unblock_user(user_id)


@router.get("/users", response_model=List[UserModelDTO])
async def get_user_models(
    limit: int = 10,
    offset: int = 0,
    user_dao: UserDAO = Depends(),
) -> List[UserModel]:
    """
    Retrieve all users objects from the database.

    :param limit: limit of users objects, defaults to 10.
    :param offset: offset of users objects, defaults to 0.
    :param user_dao: DAO for users models.
    :return: list of users objects from database.
    """
    return await user_dao.get_all_users(limit=limit, offset=offset)


@router.post("/create_admin", response_model=None)
async def create_admin(
    admin: AdminDTO,
    admin_dao: AdminDAO = Depends(),
) -> None:
    """Create an admin."""
    await admin_dao.create_admin_model(
        admin_id=admin.id,
        email=admin.email,
    )


@router.get("/admins", response_model=None)
async def get_admin_models(
    limit: int = 10,
    offset: int = 0,
    user_dao: AdminDAO = Depends(),
) -> List[AdminModel]:
    """Retrieve all admins from the database."""
    return await user_dao.get_all_admins(limit=limit, offset=offset)


@router.get("/users/{user_id}", response_model=None)
async def get_user_model(
    user_id: str,
    user_dao: UserDAO = Depends(),
) -> Optional[UserModel]:
    """Retrieve a user object from the database."""
    return await user_dao.get_user_by_id(user_id)
