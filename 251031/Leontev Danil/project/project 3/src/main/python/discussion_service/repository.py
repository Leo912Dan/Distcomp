"""
Модуль репозитория для работы с Cassandra.
Содержит методы для CRUD операций с сообщениями в базе данных.
"""

from uuid import UUID
from typing import List, Optional
from datetime import datetime

from .models import Message
from .schemas import MessageCreate, MessageUpdate

class MessageRepository:
    """
    Репозиторий для работы с сообщениями в Cassandra.
    
    Методы:
        create: Создание нового сообщения
        get: Получение сообщения по ID
        get_topic_messages: Получение всех сообщений топика
        get_user_messages: Получение всех сообщений пользователя
        update: Обновление сообщения
        delete: Удаление сообщения
    """
    
    @staticmethod
    async def create(message: MessageCreate) -> Message:
        """
        Создает новое сообщение в базе данных.
        
        Args:
            message (MessageCreate): Данные для создания сообщения
            
        Returns:
            Message: Созданное сообщение
        """
        db_message = Message(
            content=message.content,
            topic_id=message.topic_id,
            user_id=message.user_id
        )
        db_message.save()
        return db_message
    
    @staticmethod
    async def get(message_id: UUID) -> Optional[Message]:
        """
        Получает сообщение по его ID.
        
        Args:
            message_id (UUID): ID сообщения
            
        Returns:
            Optional[Message]: Найденное сообщение или None
        """
        return Message.objects.filter(id=message_id).first()
    
    @staticmethod
    async def get_topic_messages(topic_id: UUID) -> List[Message]:
        """
        Получает все сообщения для указанного топика.
        
        Args:
            topic_id (UUID): ID топика
            
        Returns:
            List[Message]: Список сообщений топика
        """
        return list(Message.objects.filter(topic_id=topic_id).all())
    
    @staticmethod
    async def get_user_messages(user_id: UUID) -> List[Message]:
        """
        Получает все сообщения указанного пользователя.
        
        Args:
            user_id (UUID): ID пользователя
            
        Returns:
            List[Message]: Список сообщений пользователя
        """
        return list(Message.objects.filter(user_id=user_id).all())
    
    @staticmethod
    async def update(message_id: UUID, message: MessageUpdate) -> Optional[Message]:
        """
        Обновляет существующее сообщение.
        
        Args:
            message_id (UUID): ID сообщения для обновления
            message (MessageUpdate): Новые данные сообщения
            
        Returns:
            Optional[Message]: Обновленное сообщение или None
        """
        db_message = await MessageRepository.get(message_id)
        if db_message:
            if message.content is not None:
                db_message.content = message.content
            db_message.updated_at = datetime.utcnow()
            db_message.save()
        return db_message
    
    @staticmethod
    async def delete(message_id: UUID) -> bool:
        """
        Удаляет сообщение по его ID.
        
        Args:
            message_id (UUID): ID сообщения для удаления
            
        Returns:
            bool: True если сообщение было удалено, False если не найдено
        """
        db_message = await MessageRepository.get(message_id)
        if db_message:
            db_message.delete()
            return True
        return False 