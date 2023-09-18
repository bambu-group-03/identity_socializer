from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
import httpx

from identity_socializer.db.dao.dummy_dao import DummyDAO
from identity_socializer.db.models.dummy_model import DummyModel
from identity_socializer.settings import settings
from identity_socializer.web.api.dummy.schema import DummyModelDTO, DummyModelInputDTO
from identity_socializer.web.api.echo.schema import Message

router = APIRouter()


@router.get("/", response_model=List[DummyModelDTO])
async def get_dummy_models(
    limit: int = 10,
    offset: int = 0,
    dummy_dao: DummyDAO = Depends(),
) -> List[DummyModel]:
    """
    Retrieve all dummy objects from the database.

    :param limit: limit of dummy objects, defaults to 10.
    :param offset: offset of dummy objects, defaults to 0.
    :param dummy_dao: DAO for dummy models.
    :return: list of dummy objects from database.
    """
    return await dummy_dao.get_all_dummies(limit=limit, offset=offset)


@router.put("/")
async def create_dummy_model(
    new_dummy_object: DummyModelInputDTO,
    dummy_dao: DummyDAO = Depends(),
) -> None:
    """
    Creates dummy model in the database.

    :param new_dummy_object: new dummy model item.
    :param dummy_dao: DAO for dummy models.
    """
    await dummy_dao.create_dummy_model(name=new_dummy_object.name)


@router.post("/tweets/tweet", response_model=Message)
def create_tweet(
    incoming_message: Message,
) -> Message:
    """
    Creates dummy tweet in content_discovery service by http.
    """
    print(f"{settings.content_discovery_url}/api/echo/")
    response = httpx.post(
        f"{settings.content_discovery_url}/api/echo/",
        json={"message": incoming_message.message},
    )
    print(response.status_code)
    return incoming_message 
