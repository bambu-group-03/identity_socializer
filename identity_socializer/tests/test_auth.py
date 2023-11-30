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


@pytest.mark.anyio
async def test_update_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests update user."""
    dao = UserDAO(dbsession)

    # Create user
    test_id = uuid.uuid4().hex
    test_email = f"{test_id}@gmail.com"

    await dao.create_user_model(
        uid=test_id,
        email=test_email,
    )

    # Update user
    url = fastapi_app.url_path_for("update_user")

    response = await client.put(
        url,
        json={
            "id": test_id,
            "first_name": "first_name_test",
            "last_name": "last_name_test",
            "username": "username_test",
            "phone_number": "phone_number_test",
            "bio_msg": "bio_msg_test",
            "profile_photo_id": "profile_photo_id_test",
            "ubication": "Argentina",
        },
    )

    instance = await dao.get_user_by_id(user_id=test_id)

    assert response.status_code == status.HTTP_200_OK

    assert instance is not None
    assert instance.email == test_email
    assert instance.first_name == "first_name_test"
    assert instance.last_name == "last_name_test"
    assert instance.username == "username_test"
    assert instance.phone_number == "phone_number_test"
    assert instance.bio_msg == "bio_msg_test"
    assert instance.profile_photo_id == "profile_photo_id_test"
    assert instance.ubication == "Argentina"


@pytest.mark.anyio
async def test_block_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests block user."""
    dao = UserDAO(dbsession)

    # Create user
    test_id = uuid.uuid4().hex
    test_email = f"{test_id}@gmail.com"

    await dao.create_user_model(
        uid=test_id,
        email=test_email,
    )

    new_user = await dao.get_user_by_id(user_id=test_id)

    assert new_user is not None
    assert new_user.blocked == False

    # Block user
    url = fastapi_app.url_path_for("block_user", user_id=new_user.id)

    response = await client.put(url)
    assert response.status_code == status.HTTP_200_OK

    user = await dao.get_user_by_id(user_id=new_user.id)
    assert user is not None
    assert user.blocked == True
