from fastapi import APIRouter, HTTPException, status
from typing import Union  # Добавьте этот импорт
from app.models import (
    WriterRequestTo, WriterResponseTo,
    NewsRequestTo, NewsResponseTo, NewsUpdateTo,
    MessageRequestTo, MessageResponseTo, MessageUpdateTo,
    LabelRequestTo, LabelResponseTo, LabelUpdateTo
)
from app.services import WriterService, NewsService, LabelService, MessageService

router = APIRouter(prefix="/api/v1.0")

# ----- Writer Endpoints -----
@router.post("/writers", response_model=WriterResponseTo, status_code=status.HTTP_201_CREATED)
def create_writer(dto: WriterRequestTo):
    return WriterService.create(dto)

@router.get("/writers", response_model=list[WriterResponseTo], status_code=status.HTTP_200_OK)
def get_all_writers():
    return WriterService.get_all()

@router.get("/writers/{id}", response_model=WriterResponseTo, status_code=status.HTTP_200_OK)
def get_writer(id: int):
    return WriterService.get_by_id(id)

@router.put("/writers", response_model=WriterResponseTo, status_code=status.HTTP_200_OK)
def update_writer(dto: WriterResponseTo):
    return WriterService.update(dto)

@router.delete("/writers/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_writer(id: int):
    return WriterService.delete(id)

@router.get("/writers/news/{news_id}", response_model=WriterResponseTo, status_code=status.HTTP_200_OK)
def get_writer_by_news(news_id: int):
    return WriterService.get_by_news_id(news_id)

# ----- News Endpoints -----
@router.post("/news", response_model=NewsResponseTo, status_code=status.HTTP_201_CREATED)
def create_news(dto: NewsRequestTo):
    return NewsService.create(dto)

@router.get("/news", response_model=list[NewsResponseTo], status_code=status.HTTP_200_OK)
def get_all_news():
    return NewsService.get_all()

@router.get("/news/{id}", response_model=NewsResponseTo, status_code=status.HTTP_200_OK)
def get_news(id: int):
    return NewsService.get_by_id(id)

@router.put("/news", response_model=NewsResponseTo, status_code=status.HTTP_200_OK)
def update_news(dto: NewsUpdateTo):
    try:
        numeric_id = int(dto.id)
    except ValueError:
        raise HTTPException(status_code=404, detail="News not found")
    update_dto = NewsRequestTo(
        writer_id=dto.writer_id,
        title=dto.title,
        content=dto.content
    )
    return NewsService.update(numeric_id, update_dto)

@router.delete("/news/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_news(id: int):
    return NewsService.delete(id)

@router.get("/news/search", response_model=NewsResponseTo, status_code=status.HTTP_200_OK)
def search_news(writer_id: Union[int, None] = None, title: Union[str, None] = None, content: Union[str, None] = None):
    search_params = {"writer_id": writer_id, "title": title, "content": content}
    return NewsService.search(**search_params)

# ----- Message Endpoints -----
@router.post("/messages", response_model=MessageResponseTo, status_code=status.HTTP_201_CREATED)
def create_message(dto: MessageRequestTo):
    return MessageService.create(dto)

@router.get("/messages", response_model=list[MessageResponseTo], status_code=status.HTTP_200_OK)
def get_all_messages():
    return MessageService.get_all()

@router.get("/messages/{id}", response_model=MessageResponseTo, status_code=status.HTTP_200_OK)
def get_message(id: int):
    return MessageService.get_by_id(id)

@router.put("/messages", response_model=MessageResponseTo, status_code=status.HTTP_200_OK)
def update_message(dto: MessageUpdateTo):
    try:
        numeric_id = int(dto.id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Message not found")
    update_dto = MessageRequestTo(
        news_id=dto.news_id,
        content=dto.content
    )
    return MessageService.update(numeric_id, update_dto)

@router.delete("/messages/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(id: int):
    return MessageService.delete(id)

@router.get("/messages/news/{news_id}", response_model=list[MessageResponseTo], status_code=status.HTTP_200_OK)
def get_messages_by_news(news_id: int):
    return MessageService.get_by_news_id(news_id)

# ----- Label Endpoints -----
@router.post("/labels", response_model=LabelResponseTo, status_code=status.HTTP_201_CREATED)
def create_label(dto: LabelRequestTo):
    return LabelService.create(dto)

@router.get("/labels", response_model=list[LabelResponseTo], status_code=status.HTTP_200_OK)
def get_all_labels():
    return LabelService.get_all()

@router.get("/labels/{id}", response_model=LabelResponseTo, status_code=status.HTTP_200_OK)
def get_label(id: int):
    return LabelService.get_by_id(id)

@router.put("/labels", response_model=LabelResponseTo, status_code=status.HTTP_200_OK)
def update_label(dto: LabelUpdateTo):
    return LabelService.update(dto.id, LabelRequestTo(name=dto.name))

@router.delete("/labels/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_label(id: int):
    return LabelService.delete(id)

@router.get("/labels/news/{news_id}", response_model=list[LabelResponseTo], status_code=status.HTTP_200_OK)
def get_labels_by_news(news_id: int):
    return LabelService.get_by_news_id(news_id)