from typing import List

from fastapi import APIRouter, Depends

from identity_socializer.db.dao.relationship_dao import RelationshipDAO
from identity_socializer.db.models.user_model import UserModel

router = APIRouter()


@router.post("/{user_id}/follow/{followed_user_id}", response_model=None)
async def follow_user(
    user_id: str,
    followed_user_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> None:
    """
    Follow a user.

    If user_id or followed_user_id does not exist, the relationship will not be created.
    """
    await relationship_dao.create_relationship_model(user_id, followed_user_id)


@router.delete("/{user_id}/unfollow/{followed_user_id}", response_model=None)
async def unfollow_user(
    user_id: str,
    followed_user_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> None:
    """
    Unfollow a user.

    Delete the relationship model between user_id and followed_user_id.
    If the relationship between user_id and followed_user_id does not exist,
    anything will happen.
    """
    await relationship_dao.delete_relationship_model(user_id, followed_user_id)


@router.get("/{user_id}/following", response_model=None)
async def get_following(
    user_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> List[UserModel]:
    """Get following of user_id."""
    return await relationship_dao.get_following_by_id(user_id)


@router.get("/{user_id}/count_following", response_model=None)
async def count_following_by_user_id(
    user_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> int:
    """Get number of following of user_id."""
    return await relationship_dao.count_following_by_user_id(user_id)


@router.get("/{user_id}/followers", response_model=None)
async def get_followers(
    user_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> List[UserModel]:
    """Get followers of user_id."""
    return await relationship_dao.get_followers_by_id(user_id)


@router.get("/{user_id}/count_followers", response_model=None)
async def count_followers_by_user_id(
    user_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> int:
    """Get number of followers of user_id."""
    return await relationship_dao.count_followers_by_user_id(user_id)
