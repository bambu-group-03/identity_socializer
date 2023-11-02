from typing import List

from fastapi import APIRouter, Depends

from identity_socializer.db.dao.user_dao import UserDAO
from identity_socializer.db.models.user_model import UserModel

router = APIRouter()


@router.get("/{username}", response_model=None)
async def filter_user(
    username: str,
    user_dao: UserDAO = Depends(),
) -> List[UserModel]:
    """Retrieve a filtered users."""
    return await user_dao.filter_user(username=username)
