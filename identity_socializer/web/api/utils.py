from typing import List

from identity_socializer.db.dao.relationship_dao import RelationshipDAO
from identity_socializer.db.models.user_model import UserModel
from identity_socializer.web.api.auth.schema import AppUserModel


async def complete_users(
    users: List[UserModel],
    current_user_id: str,
    relationship_dao: RelationshipDAO,
) -> List[AppUserModel]:
    """Returns a list of users with additional information."""
    my_users = []

    for user in users:
        completed_user = await complete_user(user, current_user_id, relationship_dao)
        my_users.append(completed_user)

    return my_users


async def complete_user(
    user: UserModel,
    current_user_id: str,
    relationship_dao: RelationshipDAO,
) -> AppUserModel:
    """Returns a user with additional information."""
    is_followed = await relationship_dao.is_followed_by_user(current_user_id, user.id)
    is_followed_back = await relationship_dao.is_followed_by_user(
        user.id,
        current_user_id,
    )

    return AppUserModel(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone_number=user.phone_number,
        bio_msg=user.bio_msg,
        profile_photo_id=user.profile_photo_id,
        ubication=user.ubication,
        is_followed=is_followed,
        is_followed_back=is_followed_back,
        blocked=user.blocked,
        certified=user.certified,
        interests=user.interests,
    )
