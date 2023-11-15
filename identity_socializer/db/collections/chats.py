from datetime import datetime

from mongoengine import DateTimeField, Document, StringField


class Chat(Document):
    """Schema for Chat."""

    owner_id = StringField(required=True)
    other_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)

    meta = {
        "collection": "chats",
    }


def get_chat(owner_id: str, other_id: str) -> str:
    """Create a chat in mongo db."""
    # Check if chat already exists
    chat = Chat.objects(owner_id=owner_id, other_id=other_id).first()

    if chat:
        return chat.id

    # Otherwise, create new chat
    new_chat = Chat(
        owner_id=owner_id,
        other_id=other_id,
    )
    new_chat.save()

    return new_chat.id
