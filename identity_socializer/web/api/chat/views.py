from typing import List

from fastapi import APIRouter, HTTPException, status
from mongoengine import connect

from identity_socializer.db.collections.chats import get_chat, get_chats_by_user_id
from identity_socializer.db.collections.messages import (
    create_message_in_chat,
    get_messages_by_chat_id,
)
from identity_socializer.settings import settings
from identity_socializer.web.api.chat.schema import ChatDTO, MessageDTO, MessageSchema

router = APIRouter()

# Create connection to mongo db
connect(
    db="identity_socializer",
    host=settings.mongo_host,
    port=27017,
)


@router.post("/send_message", response_model=None)
def send_message(
    body: MessageDTO,
) -> None:
    """
    Creates a message with the given body.

    :raises HTTPException: If something goes wrong.
    """
    try:
        # Create chat for sender
        chat_from_id = get_chat(body.from_id, body.to_id)

        # Create chat for receiver
        chat_to_id = get_chat(body.to_id, body.from_id)

        # Create message in sender chat
        create_message_in_chat(
            chat_id=chat_from_id,
            from_id=body.from_id,
            to_id=body.to_id,
            content=body.content,
        )

        # Create message in receiver chat
        create_message_in_chat(
            chat_id=chat_to_id,
            from_id=body.from_id,
            to_id=body.to_id,
            content=body.content,
        )

    except Exception as error:
        code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(error))


@router.get("/get_chats_by_user/{user_id}", response_model=None)
def get_chats(
    user_id: str,
) -> List[ChatDTO]:
    """
    Get chats for a given user.

    :raises HTTPException: If something goes wrong.
    """
    try:
        my_chats = []
        chats = get_chats_by_user_id(user_id)

        for chat in chats:

            chat_dto = ChatDTO(
                chat_id=str(chat.id),
                owner_id=chat.owner_id,
                other_id=chat.other_id,
                created_at=str(chat.created_at),
            )

            my_chats.append(chat_dto)

        return my_chats

    except Exception as error:
        code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(error))


@router.get("/get_messages_by_chat/{chat_id}")
def get_messages_by_chat(
    chat_id: str,
) -> List[MessageSchema]:
    """
    Get chats for a given user.

    :raises HTTPException: If something goes wrong.
    """
    try:
        my_messages = []
        messages = get_messages_by_chat_id(chat_id)

        for msg in messages:

            my_msg = MessageSchema(
                msg_id=str(msg.id),
                chat_id=str(msg.chat_id.id),
                from_id=msg.from_id,
                to_id=msg.to_id,
                content=msg.content,
                created_at=str(msg.created_at),
            )

            my_messages.append(my_msg)

        return my_messages

    except Exception as error:
        code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(error))
