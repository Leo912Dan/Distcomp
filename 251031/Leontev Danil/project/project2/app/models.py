from pydantic import BaseModel, Field, ConfigDict
from typing import Union, Optional
from datetime import datetime

# =============================================
# Внутренние модели (доменные объекты)
# =============================================

class User(BaseModel):
    """
    Модель пользователя системы.
    Содержит основную информацию о пользователе.
    """
    id: int  # Уникальный идентификатор пользователя
    login: str = Field(..., max_length=64)  # Логин пользователя (макс. 64 символа)
    password: str = Field(..., min_length=8, max_length=128)  # Пароль (от 8 до 128 символов)
    firstname: str = Field(..., max_length=64)  # Имя пользователя
    lastname: str = Field(..., max_length=64)  # Фамилия пользователя

class Topic(BaseModel):
    """
    Модель темы обсуждения.
    Представляет собой тему, созданную пользователем.
    """
    id: Optional[int] = None  # Уникальный идентификатор темы
    user_id: int = Field(..., alias="user_id")  # ID создателя темы
    title: str = Field(..., max_length=64)  # Заголовок темы
    content: str = Field(..., max_length=2048)  # Содержание темы
    created: datetime  # Дата и время создания
    modified: datetime  # Дата и время последнего изменения

class Mark(BaseModel):
    """
    Модель метки (тега).
    Используется для категоризации тем.
    """
    id: int  # Уникальный идентификатор метки
    name: str = Field(..., min_length=2, max_length=32)  # Название метки

class Message(BaseModel):
    """
    Модель сообщения в теме.
    Представляет собой ответ в обсуждении.
    """
    id: int  # Уникальный идентификатор сообщения
    topic_id: int = Field(..., alias="topicId")  # ID темы, к которой относится сообщение
    content: str = Field(..., max_length=2048)  # Содержание сообщения
    model_config = ConfigDict(populate_by_name=True)  # Разрешаем использование алиасов

# =============================================
# DTO для запросов (без id)
# =============================================

class UserRequestTo(BaseModel):
    """
    DTO для создания нового пользователя.
    Не содержит id, так как он генерируется автоматически.
    """
    login: str = Field(..., max_length=64)
    password: str = Field(..., min_length=8, max_length=128)
    firstname: str = Field(..., max_length=64)
    lastname: str = Field(..., max_length=64)

class TopicRequestTo(BaseModel):
    """
    DTO для создания новой темы.
    Не содержит id и временные метки.
    """
    user_id: int = Field(..., alias="userId")
    title: str = Field(..., max_length=64)
    content: str = Field(..., max_length=2048)
    model_config = ConfigDict(populate_by_name=True)

class MarkRequestTo(BaseModel):
    """
    DTO для создания новой метки.
    Содержит только название метки.
    """
    name: str = Field(..., min_length=2, max_length=32)

class MessageRequestTo(BaseModel):
    """
    DTO для создания нового сообщения.
    Не содержит id, так как он генерируется автоматически.
    """
    topic_id: int = Field(..., alias="topicId")
    content: str = Field(..., min_length=2, max_length=2048)
    model_config = ConfigDict(populate_by_name=True)

# =============================================
# DTO для ответов (с id)
# =============================================

class UserResponseTo(BaseModel):
    """
    DTO для ответа с информацией о пользователе.
    Содержит все поля пользователя, включая id.
    """
    id: int
    login: str = Field(..., max_length=64)
    password: str = Field(..., min_length=8, max_length=128)
    firstname: str = Field(..., max_length=64)
    lastname: str = Field(..., max_length=64)

class TopicResponseTo(BaseModel):
    """
    DTO для ответа с информацией о теме.
    Содержит все поля темы, включая id и временные метки.
    """
    id: int
    user_id: int = Field(..., alias="userId")
    title: str = Field(..., max_length=64)
    content: str = Field(..., max_length=2048)
    created: datetime
    modified: datetime
    model_config = ConfigDict(populate_by_name=True)

class MarkResponseTo(BaseModel):
    """
    DTO для ответа с информацией о метке.
    Содержит id и название метки.
    """
    id: int
    name: str = Field(..., min_length=2, max_length=32)

class MessageResponseTo(BaseModel):
    """
    DTO для ответа с информацией о сообщении.
    Содержит все поля сообщения, включая id.
    """
    id: int
    topic_id: int = Field(..., alias="topicId")
    content: str = Field(..., min_length=2, max_length=2048)
    model_config = ConfigDict(populate_by_name=True)

# =============================================
# DTO для обновления
# =============================================

class TopicUpdateTo(BaseModel):
    """
    DTO для обновления темы.
    Содержит все поля, которые могут быть изменены.
    """
    id: Union[str, int]  # ID может быть строкой или числом
    title: str = Field(..., max_length=64)
    content: str = Field(..., max_length=2048)
    user_id: int = Field(..., alias="userId")
    model_config = ConfigDict(populate_by_name=True)

class MessageUpdateTo(BaseModel):
    """
    DTO для обновления сообщения.
    Содержит только изменяемые поля.
    """
    id: int
    content: str = Field(..., min_length=2, max_length=2048)
    topic_id: int = Field(..., alias="topicId")
    model_config = ConfigDict(populate_by_name=True)

class MarkUpdateTo(BaseModel):
    """
    DTO для обновления метки.
    Содержит id и новое название метки.
    """
    id: int
    name: str = Field(..., min_length=2, max_length=32)
    model_config = ConfigDict(populate_by_name=True)