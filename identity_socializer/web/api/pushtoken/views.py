from fastapi import APIRouter, Depends

from identity_socializer.db.dao.push_token_dao import PushTokenDAO
from identity_socializer.web.api.pushtoken.schema import PushTokenEntry

router = APIRouter()


@router.post("/register", response_model=None)
async def push_token_register(
    body: PushTokenEntry,
    push_token_dao: PushTokenDAO = Depends(),
) -> None:
    """Register push token from user."""
    await push_token_dao.create_push_token(
        user_id=body.user_id,
        pushtoken=body.pushtoken,
    )


@router.get("/get/{user_id}", response_model=list[str])
async def get_push_tokens_by_user(
    user_id: str,
    push_token_dao: PushTokenDAO = Depends(),
) -> list[str]:
    """Get push tokens from user."""
    return await push_token_dao.get_push_tokens_by_user(
        user_id=user_id,
    )


@router.delete("/delete/{user_id}", response_model=None)
async def delete_push_tokens_by_user(
    user_id: str,
    push_token_dao: PushTokenDAO = Depends(),
) -> None:
    """Delete push tokens from user."""
    await push_token_dao.delete_push_tokens_by_user(
        user_id=user_id,
    )
