from fastapi import APIRouter
router = APIRouter()
from identity_socializer.web.api.auth.schema import Signup
from identity_socializer.web.api.auth.schema import SecurityToken

from schema import Success

@router.post("/signup", response_model=Success) 
async def signup(
    incoming_message: SecurityToken,
) -> SecurityToken:
  import firebase_admin
  from firebase_admin import credentials
  from firebase_admin import auth
  cred = credentials.Certificate("identity_socializer/firebase_credentials.json")
  firebase_admin.initialize_app(cred)

  user = auth.getUser(incoming_message.token)
  print('Successfully fetched user data: {0}'.format(user.uid))

  custom_token = auth.create_custom_token(user.uid)
  ret = Success("todo fino")
  return ret