import firebase_admin
import pytest
from fastapi import FastAPI
from firebase_admin import credentials
from httpx import AsyncClient


@pytest.mark.anyio
async def test_successfully_signup(client: AsyncClient, fastapi_app: FastAPI) -> None:
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)


# Client creates user and returns token from firebase admin


# Client sends token to server


# server get user from firebase by token


# server verifies user in


@pytest.mark.anyio
async def test_successfully_signin(client: AsyncClient) -> None:
    pass
