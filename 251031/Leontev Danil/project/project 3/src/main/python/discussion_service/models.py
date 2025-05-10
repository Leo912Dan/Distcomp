"""
Модуль моделей данных для Cassandra.
Определяет структуру таблиц и их связи в базе данных.
"""

from datetime import datetime
from uuid import UUID, uuid4
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Message(Model):
    """
    Модель сообщения в Cassandra.
    
    Атрибуты:
        id (UUID): Уникальный идентификатор сообщения
        content (Text): Текст сообщения
        topic_id (UUID): ID топика, к которому относится сообщение
        user_id (UUID): ID пользователя, создавшего сообщение
        created_at (DateTime): Время создания сообщения
        updated_at (DateTime): Время последнего обновления сообщения
    """
    # Указываем keyspace и имя таблицы
    __keyspace__ = 'discussion'
    __table_name__ = 'messages'
    
    # Определяем колонки таблицы
    id = columns.UUID(primary_key=True, default=uuid4)  # Первичный ключ
    content = columns.Text(required=True)  # Текст сообщения
    topic_id = columns.UUID(required=True, index=True)  # ID топика с индексом для быстрого поиска
    user_id = columns.UUID(required=True, index=True)  # ID пользователя с индексом для быстрого поиска
    created_at = columns.DateTime(default=datetime.utcnow)  # Время создания
    updated_at = columns.DateTime(default=datetime.utcnow)  # Время обновления 