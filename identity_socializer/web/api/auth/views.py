from fastapi import APIRouter
router = APIRouter()
from identity_socializer.web.api.auth.schema import Signup
from identity_socializer.web.api.auth.schema import SecurityToken

@router.post("/signup", response_model=SecurityToken) 
async def signup(
    incoming_message: Signup,
) -> SecurityToken:
  assert incoming_message.username 
  ret = SecurityToken(token="my token super secreta")
  return ret