from datetime import datetime
from typing import List

from mongoengine import DateTimeField, Document, ReferenceField, StringField

from identity_socializer.db.collections.chats import Chat
from identity_socializer.db.utils import is_valid_mongo_id


class Message(Document):
    """Schema for Message."""

    chat_id = ReferenceField(Chat)
    from_id = StringField(required=True)
    to_id = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=lambda: datetime.now())

    meta = {
        "collection": "messages",
    }


def create_message_in_chat(
    from_id: str,
    to_id: str,
    content: str,
    chat_id: str,
) -> Message:
    """Create a message in mongo db."""
    new_message = Message(
        chat_id=chat_id,
        from_id=from_id,
        to_id=to_id,
        content=content,
    )
    new_message.save()

    return new_message


def get_messages_by_chat_id(chat_id: str) -> List[Message]:
    """Get messages by chat id."""
    if not is_valid_mongo_id(chat_id):
        return []

    return Message.objects.filter(chat_id=chat_id)
