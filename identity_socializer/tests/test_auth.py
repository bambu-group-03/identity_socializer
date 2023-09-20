import pytest
from fastapi import FastAPI
from firebase_admin import credentials, initialize_app
from httpx import AsyncClient


@pytest.mark.anyio
async def test_successfully_signup(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """Test successfully signup."""
    cred = credentials.Certificate("firebase_credentials.json")
    initialize_app(cred)


# Client creates user and returns token from firebase admin


# Client sends token to server


# server get user from firebase by token


# server verifies user in


# TODO fix this test
# @pytest.mark.anyio
# async def test_successfully_signin(client: AsyncClient) -> None:
#     pass
