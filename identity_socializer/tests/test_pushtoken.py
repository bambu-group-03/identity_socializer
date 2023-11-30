import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from identity_socializer.db.dao.push_token_dao import PushTokenDAO


@pytest.mark.anyio
async def test_register_single_push_token(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests user register push tokens."""
    dao = PushTokenDAO(dbsession)

    test_id = uuid.uuid4().hex
    test_pushtoken = uuid.uuid4().hex

    instances = await dao.get_push_tokens_by_user(user_id=test_id)
    assert not instances

    url = fastapi_app.url_path_for("push_token_register")
    response = await client.post(
        url,
        json={
            "user_id": test_id,
            "pushtoken": test_pushtoken,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    instances = await dao.get_push_tokens_by_user(user_id=test_id)

    assert len(instances) == 1
    assert instances[0] == test_pushtoken


@pytest.mark.anyio
async def test_register_multiple_push_token(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests user register multiple push tokens."""
    dao = PushTokenDAO(dbsession)

    test_id = uuid.uuid4().hex
    test_pushtoken1 = uuid.uuid4().hex
    test_pushtoken2 = uuid.uuid4().hex

    url = fastapi_app.url_path_for("push_token_register")

    response = await client.post(
        url,
        json={
            "user_id": test_id,
            "pushtoken": test_pushtoken1,
        },
    )

    response = await client.post(
        url,
        json={
            "user_id": test_id,
            "pushtoken": test_pushtoken2,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    instances = await dao.get_push_tokens_by_user(user_id=test_id)

    assert len(instances) == 2
    assert instances[0] == test_pushtoken1
    assert instances[1] == test_pushtoken2


# TODO fix this test
# @pytest.mark.anyio
# async def test_register_repeated_push_token(
#     fastapi_app: FastAPI,
#     client: AsyncClient,
#     dbsession: AsyncSession,
# ) -> None:
#     """Tests user register repeated push tokens."""
#     dao = PushTokenDAO(dbsession)

#     test_id = uuid.uuid4().hex
#     test_pushtoken1 = uuid.uuid4().hex

#     url = fastapi_app.url_path_for("push_token_register")

#     response = await client.post(
#         url,
#         json={
#             "user_id": test_id,
#             "pushtoken": test_pushtoken1,
#         },
#     )

#     response = await client.post(
#         url,
#         json={
#             "user_id": test_id,
#             "pushtoken": test_pushtoken1,
#         },
#     )

#     assert response.status_code == status.HTTP_200_OK

#     instances = await dao.get_push_tokens_by_user(user_id=test_id)

#     assert len(instances) == 1
#     assert instances[0] == test_pushtoken1
