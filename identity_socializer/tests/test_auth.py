import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from identity_socializer.db.dao.user_dao import UserDAO


@pytest.mark.anyio
async def test_register(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests user model instance creation."""
    url = fastapi_app.url_path_for("register")

    test_id = uuid.uuid4().hex
    test_email = f"{test_id}@gmail.com"

    response = await client.post(
        url,
        json={
            "id": test_id,
            "email": test_email,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    dao = UserDAO(dbsession)
    instance = await dao.get_user_by_id(user_id=test_id)

    assert instance is not None
    assert instance.email == test_email
