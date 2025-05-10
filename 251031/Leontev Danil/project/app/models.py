from pydantic import BaseModel, Field, ConfigDict
from typing import Union, Optional
from datetime import datetime

# ----- Доменные модели -----
# Базовые модели, представляющие сущности в системе

class User(BaseModel):
    """Модель пользователя системы"""
    id: int
    login: str = Field(..., max_length=64)  # Уникальный логин
    password: str = Field(..., min_length=8, max_length=128)  # Пароль с ограничениями
    firstname: str = Field(..., max_length=64)  # Имя
    lastname: str = Field(..., max_length=64)  # Фамилия

class Topic(BaseModel):
    """Модель темы/обсуждения"""
    id: Optional[int] = None
    user_id: int = Field(..., alias="user_id")  # ID создателя темы
    title: str = Field(..., max_length=64)  # Заголовок темы
    content: str = Field(..., max_length=2048)  # Содержание темы
    created: datetime  # Дата создания
    modified: datetime  # Дата последнего изменения

class Mark(BaseModel):
    """Модель метки/тега"""
    id: int
    name: str = Field(..., min_length=2, max_length=32)  # Название метки

class Message(BaseModel):
    """Модель сообщения в теме"""
    id: int
    topic_id: int = Field(..., alias="topicId")  # ID темы
    content: str = Field(..., max_length=2048)  # Содержание сообщения
    model_config = ConfigDict(populate_by_name=True)  # Разрешаем использовать snake_case в коде

# ----- DTO для запросов -----
# Модели для входящих данных (без id)

class UserRequestTo(BaseModel):
    """DTO для создания пользователя"""
    login: str = Field(..., max_length=64)
    password: str = Field(..., min_length=8, max_length=128)
    firstname: str = Field(..., max_length=64)
    lastname: str = Field(..., max_length=64)

class TopicRequestTo(BaseModel):
    """DTO для создания темы"""
    user_id: int = Field(..., alias="userId")  # camelCase для JSON
    title: str = Field(..., max_length=64)
    content: str = Field(..., max_length=2048)
    model_config = ConfigDict(populate_by_name=True)

class MarkRequestTo(BaseModel):
    """DTO для создания метки"""
    name: str = Field(..., min_length=2, max_length=32)

class MessageRequestTo(BaseModel):
    """DTO для создания сообщения"""
    topic_id: int = Field(..., alias="topicId")  # camelCase для JSON
    content: str = Field(..., min_length=2, max_length=2048)
    model_config = ConfigDict(populate_by_name=True)

# ----- DTO для ответов -----
# Модели для исходящих данных (с id)

class UserResponseTo(BaseModel):
    """DTO для ответа с данными пользователя"""
    id: int
    login: str = Field(..., max_length=64)
    password: str = Field(..., min_length=8, max_length=128)
    firstname: str = Field(..., max_length=64)
    lastname: str = Field(..., max_length=64)

class TopicResponseTo(BaseModel):
    """DTO для ответа с данными темы"""
    id: int
    user_id: int = Field(..., alias="userId")  # camelCase для JSON
    title: str = Field(..., max_length=64)
    content: str = Field(..., max_length=2048)
    created: datetime
    modified: datetime
    model_config = ConfigDict(populate_by_name=True)

class MarkResponseTo(BaseModel):
    """DTO для ответа с данными метки"""
    id: int
    name: str = Field(..., min_length=2, max_length=32)

class MessageResponseTo(BaseModel):
    """DTO для ответа с данными сообщения"""
    id: int
    topic_id: int = Field(..., alias="topicId")  # camelCase для JSON
    content: str = Field(..., min_length=2, max_length=2048)
    model_config = ConfigDict(populate_by_name=True)

# ----- DTO для обновления -----
# Модели для обновления существующих сущностей

class TopicUpdateTo(BaseModel):
    """DTO для обновления темы"""
    id: Union[str, int]  # ID может быть строкой или числом
    title: str = Field(..., max_length=64)
    content: str = Field(..., max_length=2048)
    user_id: int = Field(..., alias="userId")
    model_config = ConfigDict(populate_by_name=True)

class MessageUpdateTo(BaseModel):
    """DTO для обновления сообщения"""
    id: int
    content: str = Field(..., min_length=2, max_length=2048)
    topic_id: int = Field(..., alias="topicId")
    model_config = ConfigDict(populate_by_name=True)

class MarkUpdateTo(BaseModel):
    """DTO для обновления метки"""
    id: int
    name: str = Field(..., min_length=2, max_length=32)
    model_config = ConfigDict(populate_by_name=True)