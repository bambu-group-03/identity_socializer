from datetime import datetime

from mongoengine import DateTimeField, Document, ReferenceField, StringField

from identity_socializer.db.collections.chats import Chat


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
) -> None:
    """Create a message in mongo db."""
    new_message = Message(
        chat_id=chat_id,
        from_id=from_id,
        to_id=to_id,
        content=content,
    )
    new_message.save()
