from typing import List, Optional
from uuid import UUID
from .models import Message
from .schemas import MessageCreate, MessageUpdate
from datetime import datetime

class MessageRepository:
    @staticmethod
    async def create(message: MessageCreate) -> Message:
        db_message = Message(
            content=message.content,
            topic_id=message.topic_id,
            user_id=message.user_id
        )
        db_message.save()
        return db_message

    @staticmethod
    async def get(message_id: UUID) -> Optional[Message]:
        return Message.objects.filter(id=message_id).first()

    @staticmethod
    async def get_by_topic(topic_id: UUID) -> List[Message]:
        return list(Message.objects.filter(topic_id=topic_id).all())

    @staticmethod
    async def update(message_id: UUID, message: MessageUpdate) -> Optional[Message]:
        db_message = await MessageRepository.get(message_id)
        if not db_message:
            return None
        
        if message.content is not None:
            db_message.content = message.content
            db_message.updated_at = datetime.utcnow()
            db_message.save()
        
        return db_message

    @staticmethod
    async def delete(message_id: UUID) -> bool:
        message = await MessageRepository.get(message_id)
        if message:
            message.delete()
            return True
        return False 