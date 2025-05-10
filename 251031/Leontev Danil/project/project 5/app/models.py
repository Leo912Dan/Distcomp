from pydantic import BaseModel, Field, ConfigDict
from typing import Union
from datetime import datetime

# Внутренние модели (доменные объекты)
class Writer(BaseModel):
    id: int
    login: str
    password: str
    firstname: str
    lastname: str

class News(BaseModel):
    id: int
    writer_id: int
    title: str
    content: str
    created: datetime
    modified: datetime

class Label(BaseModel):
    id: int
    name: str

class Message(BaseModel):
    id: int
    news_id: int
    content: str

# DTO для запросов (без id)
class WriterRequestTo(BaseModel):
    login: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    firstname: str = Field(..., min_length=1)
    lastname: str = Field(..., min_length=1)

class NewsRequestTo(BaseModel):
    writer_id: int = Field(..., alias="writerId")
    title: str
    content: str

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

class LabelRequestTo(BaseModel):
    name: str = Field(..., min_length=2, max_length=32)

class MessageRequestTo(BaseModel):
    news_id: Union[int, str] = Field(..., alias="newsId")
    content: str = Field(..., min_length=2, max_length=2048)

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

# DTO для ответов (с id)
class WriterResponseTo(BaseModel):
    id: int
    login: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    firstname: str = Field(..., min_length=1)
    lastname: str = Field(..., min_length=1)

class NewsResponseTo(BaseModel):
    id: int
    writer_id: int = Field(..., alias="writerId")
    title: str
    content: str
    created: datetime
    modified: datetime

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

class LabelResponseTo(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=32)

class MessageResponseTo(BaseModel):
    id: int
    news_id: int = Field(..., alias="newsId")
    content: str = Field(..., min_length=2, max_length=2048)

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

# DTO для обновления News – id может быть числом или строкой
class NewsUpdateTo(BaseModel):
    id: Union[str, int]
    title: str
    content: str
    writer_id: int = Field(..., alias="writerId")

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

# DTO для обновления Message – включает id
class MessageUpdateTo(BaseModel):
    id: int
    content: str
    news_id: Union[int, str] = Field(..., alias="newsId")

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name

# DTO для обновления Label – включает id
class LabelUpdateTo(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(populate_by_name=True)  # Замена allow_population_by_field_name