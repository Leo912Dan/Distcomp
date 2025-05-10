from typing import List
from fastapi import HTTPException
from app.models.message import MessageCreate, MessageUpdate, Message
from app.services.kafka_service import kafka_service
from app.config.kafka import MESSAGE_STATES

class MessageService:
    @staticmethod
    async def create(message: MessageCreate) -> Message:
        # Создаем сообщение в базе данных
        db_message = Message(
            content=message.content,
            topic_id=message.topic_id,
            user_id=message.user_id,
            state=MESSAGE_STATES["PENDING"]
        )
        # TODO: Сохранить в базу данных
        
        # Отправляем сообщение в Kafka
        await kafka_service.send_message(db_message)
        
        return db_message

    @staticmethod
    async def update(message_id: int, message_update: MessageUpdate) -> Message:
        # Получаем сообщение из базы данных
        # TODO: Получить из базы данных
        db_message = None
        
        if not db_message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Обновляем поля
        if message_update.content is not None:
            db_message.content = message_update.content
        if message_update.state is not None:
            db_message.state = message_update.state
            
        # TODO: Сохранить в базу данных
        
        return db_message

    @staticmethod
    async def get_by_id(message_id: int) -> Message:
        # TODO: Получить из базы данных
        message = None
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        return message

    @staticmethod
    async def get_all() -> List[Message]:
        # TODO: Получить все сообщения из базы данных
        return []

    @staticmethod
    async def delete(message_id: int) -> None:
        # TODO: Удалить из базы данных
        pass 