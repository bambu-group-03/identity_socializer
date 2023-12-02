from typing import List

from fastapi import APIRouter, Depends, HTTPException

from identity_socializer.db.dao.push_token_dao import PushTokenDAO
from identity_socializer.db.dao.relationship_dao import RelationshipDAO
from identity_socializer.db.dao.user_dao import UserDAO
from identity_socializer.services.push_notifications import PushNotifications
from identity_socializer.web.api.auth.schema import AppUserModel
from identity_socializer.web.api.utils import complete_users

router = APIRouter()

push_notifications = PushNotifications()


@router.post("/{from_id}/follow/{followed_user_id}", response_model=None)
async def follow_user(
    from_id: str,
    to_id: str,
    user_dao: UserDAO = Depends(),
    relationship_dao: RelationshipDAO = Depends(),
    push_token_dao: PushTokenDAO = Depends(),
) -> None:
    """
    Follow a user.

    If user_id or followed_user_id does not exist, the relationship will not be created.
    """
    relationship = await relationship_dao.create_relationship_model(
        from_id,
        to_id,
    )

    if relationship is None:
        return

    # Notify the followed user
    await push_notifications.new_follower(
        from_id,
        to_id,
        user_dao,
        relationship_dao,
        push_token_dao,
    )


@router.delete("/{from_id}/unfollow/{to_id}", response_model=None)
async def unfollow_user(
    from_id: str,
    to_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> None:
    """
    Unfollow a user.

    Delete the relationship model between user_id and followed_user_id.
    If the relationship between user_id and followed_user_id does not exist,
    anything will happen.
    """
    await relationship_dao.delete_relationship_model(from_id, to_id)


@router.get("/{user_id}/mutuals_with/{another_id}")
async def is_mutuals(
    user_id: str,
    another_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> bool:
    """True if both users are mutually following each other."""
    return await relationship_dao.is_mutuals(user_id, another_id)


@router.get("/{user_id}/following", response_model=None)
async def get_following(
    user_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> List[AppUserModel]:
    """Get following of user_id."""
    following = await relationship_dao.get_following_by_id(user_id)
    return await complete_users(following, user_id, relationship_dao)


@router.get("/{user_id}/following/requested_by/{requesting_id}", response_model=None)
async def get_following_requested(
    user_id: str,
    requesting_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> List[AppUserModel]:
    """
    Get following of user_id if reuesting_id is authorized to view it.

    :raises HTTPException: If something goes wrong.
    """
    mutuals = await relationship_dao.is_mutuals(user_id, requesting_id)
    if not (mutuals or (user_id == requesting_id)):
        raise HTTPException(status_code=401, detail="User not authorized to view")
    following = await relationship_dao.get_following_by_id(user_id)
    return await complete_users(following, user_id, relationship_dao)


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
) -> List[AppUserModel]:
    """Get followers of user_id."""
    followers = await relationship_dao.get_followers_by_id(user_id)
    return await complete_users(followers, user_id, relationship_dao)


@router.get("/{user_id}/followers/requested_by/{requesting_id}", response_model=None)
async def get_followers_requested(
    user_id: str,
    requesting_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> List[AppUserModel]:
    """
    Get followers of user_id.

    :raises HTTPException: If something goes wrong.
    """
    mutuals = await relationship_dao.is_mutuals(user_id, requesting_id)
    if not (mutuals or (user_id == requesting_id)):
        raise HTTPException(status_code=401, detail="User not authorized to view")
    followers = await relationship_dao.get_followers_by_id(user_id)
    return await complete_users(followers, user_id, relationship_dao)


@router.get("/{user_id}/count_followers", response_model=None)
async def count_followers_by_user_id(
    user_id: str,
    relationship_dao: RelationshipDAO = Depends(),
) -> int:
    """Get number of followers of user_id."""
    return await relationship_dao.count_followers_by_user_id(user_id)
