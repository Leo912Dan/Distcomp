from fastapi import APIRouter, HTTPException, status, Depends
from typing import Union  # Добавьте этот импорт
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import (
    WriterRequestTo, WriterResponseTo,
    NewsRequestTo, NewsResponseTo,
    MessageRequestTo, MessageResponseTo,
    LabelRequestTo, LabelResponseTo
)
from app.services import WriterService, NewsService, LabelService, MessageService
from app.db import get_session  # Функция для получения сессии

router = APIRouter(prefix="/api/v1.0")

# ----- Writer Endpoints -----
@router.post("/writers", response_model=WriterResponseTo, status_code=status.HTTP_201_CREATED)
async def create_writer(dto: WriterRequestTo, session: AsyncSession = Depends(get_session)):
    return await WriterService.create(session, dto)

@router.get("/writers", response_model=list[WriterResponseTo], status_code=status.HTTP_200_OK)
async def get_all_writers(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    return await WriterService.get_all(session, skip, limit)

@router.get("/writers/{id}", response_model=WriterResponseTo, status_code=status.HTTP_200_OK)
async def get_writer(id: int, session: AsyncSession = Depends(get_session)):
    return await WriterService.get_by_id(session, id)

@router.put("/writers/{id}", response_model=WriterResponseTo, status_code=status.HTTP_200_OK)
async def update_writer(id: int, dto: WriterRequestTo, session: AsyncSession = Depends(get_session)):
    return await WriterService.update(session, id, dto)

@router.delete("/writers/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_writer(id: int, session: AsyncSession = Depends(get_session)):
    await WriterService.delete(session, id)

@router.get("/writers/news/{news_id}", response_model=WriterResponseTo, status_code=status.HTTP_200_OK)
def get_writer_by_news(news_id: int):
    return WriterService.get_by_news_id(news_id)

# ----- News Endpoints -----
@router.post("/news", response_model=NewsResponseTo, status_code=status.HTTP_201_CREATED)
async def create_news(dto: NewsRequestTo, session: AsyncSession = Depends(get_session)):
    return await NewsService.create(session, dto)

@router.get("/news", response_model=list[NewsResponseTo], status_code=status.HTTP_200_OK)
async def get_all_news(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    sort_order: str = "asc",
    title: str = None,
    session: AsyncSession = Depends(get_session)
):
    return await NewsService.get_all(session, skip, limit, sort_by, sort_order, title)

@router.get("/news/{id}", response_model=NewsResponseTo, status_code=status.HTTP_200_OK)
async def get_news(id: int, session: AsyncSession = Depends(get_session)):
    return await NewsService.get_by_id(session, id)

@router.put("/news/{id}", response_model=NewsResponseTo, status_code=status.HTTP_200_OK)
async def update_news(id: int, dto: NewsRequestTo, session: AsyncSession = Depends(get_session)):
    return await NewsService.update(session, id, dto)

@router.delete("/news/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(id: int, session: AsyncSession = Depends(get_session)):
    await NewsService.delete(session, id)

@router.get("/news/search", response_model=NewsResponseTo, status_code=status.HTTP_200_OK)
def search_news(writer_id: Union[int, None] = None, title: Union[str, None] = None, content: Union[str, None] = None):
    search_params = {"writer_id": writer_id, "title": title, "content": content}
    return NewsService.search(**search_params)

# ----- Message Endpoints -----
@router.post("/messages", response_model=MessageResponseTo, status_code=status.HTTP_201_CREATED)
async def create_message(dto: MessageRequestTo, session: AsyncSession = Depends(get_session)):
    return await MessageService.create(session, dto)

@router.get("/messages", response_model=list[MessageResponseTo], status_code=status.HTTP_200_OK)
async def get_all_messages(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    return await MessageService.get_all(session, skip, limit)

@router.get("/messages/{id}", response_model=MessageResponseTo, status_code=status.HTTP_200_OK)
async def get_message(id: int, session: AsyncSession = Depends(get_session)):
    return await MessageService.get_by_id(session, id)

@router.put("/messages/{id}", response_model=MessageResponseTo, status_code=status.HTTP_200_OK)
async def update_message(id: int, dto: MessageRequestTo, session: AsyncSession = Depends(get_session)):
    return await MessageService.update(session, id, dto)

@router.delete("/messages/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(id: int, session: AsyncSession = Depends(get_session)):
    await MessageService.delete(session, id)

@router.get("/messages/news/{news_id}", response_model=list[MessageResponseTo], status_code=status.HTTP_200_OK)
def get_messages_by_news(news_id: int):
    return MessageService.get_by_news_id(news_id)

# ----- Label Endpoints -----
@router.post("/labels", response_model=LabelResponseTo, status_code=status.HTTP_201_CREATED)
async def create_label(dto: LabelRequestTo, session: AsyncSession = Depends(get_session)):
    return await LabelService.create(session, dto)

@router.get("/labels", response_model=list[LabelResponseTo], status_code=status.HTTP_200_OK)
async def get_all_labels(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    return await LabelService.get_all(session, skip, limit)

@router.get("/labels/{id}", response_model=LabelResponseTo, status_code=status.HTTP_200_OK)
async def get_label(id: int, session: AsyncSession = Depends(get_session)):
    return await LabelService.get_by_id(session, id)

@router.put("/labels/{id}", response_model=LabelResponseTo, status_code=status.HTTP_200_OK)
async def update_label(id: int, dto: LabelRequestTo, session: AsyncSession = Depends(get_session)):
    return await LabelService.update(session, id, dto)

@router.delete("/labels/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_label(id: int, session: AsyncSession = Depends(get_session)):
    await LabelService.delete(session, id)

@router.get("/labels/news/{news_id}", response_model=list[LabelResponseTo], status_code=status.HTTP_200_OK)
def get_labels_by_news(news_id: int):
    return LabelService.get_by_news_id(news_id)