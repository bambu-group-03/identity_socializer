from fastapi import APIRouter, HTTPException
from firebase_admin import auth, credentials, initialize_app

from identity_socializer.web.api.auth.schema import SecurityToken, Success

router = APIRouter()

CRED = credentials.Certificate("identity_socializer/firebase_credentials.json")
initialize_app(CRED)


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
