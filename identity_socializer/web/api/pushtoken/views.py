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
