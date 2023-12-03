from typing import List

from fastapi import APIRouter, Depends

from identity_socializer.db.dao.relationship_dao import RelationshipDAO
from identity_socializer.db.dao.user_dao import UserDAO
from identity_socializer.db.models.user_model import UserModel
from identity_socializer.web.api.auth.schema import AppUserModel
from identity_socializer.web.api.utils import complete_users

router = APIRouter()


@router.get("/admin/{username}", response_model=None)
async def admin_filter_user(
    username: str,
    user_dao: UserDAO = Depends(),
) -> List[UserModel]:
    """Retrieve a filtered users."""
    return await user_dao.filter_user(username)


@router.get("/{current_user_id}/{username}", response_model=None)
async def filter_user(
    username: str,
    current_user_id: str,
    user_dao: UserDAO = Depends(),
    relationship_dao: RelationshipDAO = Depends(),
) -> List[AppUserModel]:
    """Retrieve a filtered users."""
    users = await user_dao.filter_user(username=username)

    return await complete_users(users, current_user_id, relationship_dao)
