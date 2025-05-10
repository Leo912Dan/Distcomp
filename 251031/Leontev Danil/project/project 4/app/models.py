from pydantic import BaseModel, Field, ConfigDict
from typing import Union
from datetime import datetime

# Внутренние модели (доменные объекты)
class User(BaseModel):
    id: int
    login: str
    password: str
    firstname: str
    lastname: str

class Topic(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created: datetime
    modified: datetime

class Mark(BaseModel):
    id: int
    name: str

class Message(BaseModel):
    id: int
    topic_id: int
    content: str

# DTO для запросов (без id)
class UserRequestTo(BaseModel):
    login: str = Field(..., min_length=2)
    password: str = Field(..., min_length=2)
    firstname: str = Field(..., min_length=2)
    lastname: str = Field(..., min_length=2)

class TopicRequestTo(BaseModel):
    user_id: int = Field(..., alias="userId")
    title: str
    content: str

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

class MarkRequestTo(BaseModel):
    name: str

class MessageRequestTo(BaseModel):
    topic_id: Union[int, str] = Field(..., alias="topicId")
    content: str

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

# DTO для ответов (с id)
class UserResponseTo(BaseModel):
    id: int
    login: str
    password: str
    firstname: str
    lastname: str

class TopicResponseTo(BaseModel):
    id: int
    user_id: int = Field(..., alias="userId")
    title: str
    content: str

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

class MarkResponseTo(BaseModel):
    id: int
    name: str

class MessageResponseTo(BaseModel):
    id: int
    topic_id: int = Field(..., alias="topicId")
    content: str

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

# DTO для обновления Topic – id может быть числом или строкой
class TopicUpdateTo(BaseModel):
    id: Union[int, str]
    user_id: int = Field(..., alias="userId")
    title: str
    content: str

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

# DTO для обновления Message – включает id
class MessageUpdateTo(BaseModel):
    id: int
    content: str
    topic_id: Union[int, str] = Field(..., alias="topicId")

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

# DTO для обновления Mark – включает id
class MarkUpdateTo(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name