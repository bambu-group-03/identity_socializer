import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from identity_socializer.db.dao.admin_dao import AdminDAO
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


@pytest.mark.anyio
async def test_unblock_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests unblock user."""
    dao = UserDAO(dbsession)

    # Create user
    test_id = uuid.uuid4().hex
    test_email = f"{test_id}@gmail.com"

    await dao.create_user_model(
        uid=test_id,
        email=test_email,
    )

    # Block user
    await dao.block_user(test_id)

    new_user = await dao.get_user_by_id(user_id=test_id)

    assert new_user is not None
    assert new_user.blocked == True

    # Unblock user
    url = fastapi_app.url_path_for("unblock_user", user_id=new_user.id)

    response = await client.put(url)
    assert response.status_code == status.HTTP_200_OK

    user = await dao.get_user_by_id(user_id=new_user.id)
    assert user is not None
    assert user.blocked == False


@pytest.mark.anyio
async def test_getting_users(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests users instance retrieval."""
    dao = UserDAO(dbsession)

    url = fastapi_app.url_path_for("get_user_models")
    response = await client.get(url)
    users = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert not users

    # Create user
    test_id1 = uuid.uuid4().hex
    test_email1 = f"{test_id1}@gmail.com"

    await dao.create_user_model(
        uid=test_id1,
        email=test_email1,
    )

    test_id2 = uuid.uuid4().hex
    test_email2 = f"{test_id2}@gmail.com"

    await dao.create_user_model(
        uid=test_id2,
        email=test_email2,
    )

    response = await client.get(url)
    users = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(users) == 2
    assert users[0]["id"] == test_id1
    assert users[1]["id"] == test_id2


@pytest.mark.anyio
async def test_create_admin(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests admin model instance creation."""
    url = fastapi_app.url_path_for("create_admin")

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
    dao = AdminDAO(dbsession)
    instances = await dao.get_all_admins(limit=10, offset=0)

    assert len(instances) == 1
    assert instances[0].id == test_id
    assert instances[0].email == test_email


@pytest.mark.anyio
async def test_getting_admins(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests admins instance retrieval."""
    dao = AdminDAO(dbsession)

    url = fastapi_app.url_path_for("get_admin_models")
    response = await client.get(url)
    admins = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert not admins

    # Create admins
    test_id1 = uuid.uuid4().hex
    test_email1 = f"{test_id1}@gmail.com"

    await dao.create_admin_model(
        admin_id=test_id1,
        email=test_email1,
    )

    test_id2 = uuid.uuid4().hex
    test_email2 = f"{test_id2}@gmail.com"

    await dao.create_admin_model(
        admin_id=test_id2,
        email=test_email2,
    )

    response = await client.get(url)
    admins = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(admins) == 2
    assert admins[0]["id"] == test_id1
    assert admins[1]["id"] == test_id2


@pytest.mark.anyio
async def test_getting_user_by_username(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests user by username instance retrieval."""
    dao = UserDAO(dbsession)

    # Create user
    test_id1 = uuid.uuid4().hex
    test_email1 = f"{test_id1}@gmail.com"

    await dao.create_user_model(
        uid=test_id1,
        email=test_email1,
        username="test_username",
    )

    url = fastapi_app.url_path_for("get_user_by_username", username="test_username")
    response = await client.get(url)

    user = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert user is not None
    assert user["id"] == test_id1
    assert user["email"] == test_email1
    assert user["username"] == "test_username"
