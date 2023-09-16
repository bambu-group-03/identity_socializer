from fastapi import APIRouter
router = APIRouter()
from identity_socializer.web.api.auth.schema import SecurityToken, Success

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
CRED = credentials.Certificate("identity_socializer/firebase_credentials.json")
firebase_admin.initialize_app(CRED)

@router.post("/signup", response_model=Success) 
async def signup(
    incoming_message: SecurityToken,
) -> Success:
  ret = Success(msg="Success")
  try:
    res = auth.verify_id_token(incoming_message.token)
    print(res)
  except auth.InvalidIdTokenError:
    ret = Success(msg="InvalidIdTokenError")
  return ret