from fastapi import APIRouter
router = APIRouter()
from identity_socializer.web.api.auth.schema import Signup
from identity_socializer.web.api.auth.schema import SecurityToken


@router.post("/signup", response_model=SecurityToken) 
async def signup(
    incoming_message: Signup,
) -> SecurityToken:
  assert incoming_message.username 

  import firebase_admin
  from firebase_admin import credentials
  from firebase_admin import auth
  cred = credentials.Certificate("identity_socializer/firebase_credentials.json")
  firebase_admin.initialize_app(cred)

  user = auth.create_user(
    email=incoming_message.email,
    email_verified=False,
    password=incoming_message.password,
    disabled=False)
  print('Sucessfully created new user: {0}'.format(user.uid))


  ret = SecurityToken("Juanito alimaña")
  return ret