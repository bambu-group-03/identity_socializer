from fastapi import APIRouter, HTTPException, status
from mongoengine import connect

from identity_socializer.db.collections.chats import get_chat
from identity_socializer.db.collections.messages import create_message_in_chat
from identity_socializer.web.api.chat.schema import MessageDTO

router = APIRouter()


@router.post("/create_message", response_model=None)
def create_message(
    body: MessageDTO,
) -> None:
    """
    Creates a message with the given body.

    :raises HTTPException: If something goes wrong.
    """
    port = 27017

    connect(
        db="identity_socializer",
        host="mongodb://identity_socializer-mongo-db-1",
        port=port,
    )

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
