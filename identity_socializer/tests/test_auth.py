import pytest
from httpx import AsyncClient
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

@pytest.mark.anyio
async def test_successfully_signup(client: AsyncClient, fastapi_app: FastAPI) -> None:
  cred = credentials.Certificate("identity_socializer/firebase_credentials.json")
  firebase_admin.initialize_app(cred)


@pytest.mark.anyio
async def test_successfully_signin(client: AsyncClient) -> None:
    pass


