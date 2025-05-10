from fastapi import HTTPException, status
from datetime import datetime
from app.models import Writer, News, Label, Message
from app.schemas import (
    WriterRequestTo, WriterResponseTo,
    NewsRequestTo, NewsResponseTo,
    LabelRequestTo, LabelResponseTo,
    MessageRequestTo, MessageResponseTo
)
from app.repositories import WriterRepository, NewsRepository, LabelRepository, MessageRepository
from sqlalchemy import select, asc, desc

# Сервис для Writer
class WriterService:
    @staticmethod
    async def create(session, dto: WriterRequestTo) -> WriterResponseTo:
        writer = Writer(**dto.dict())
        writer = await WriterRepository.create(session, writer)
        return WriterResponseTo(**writer.__dict__)

    @staticmethod
    async def get_by_id(session, id: int) -> WriterResponseTo:
        writer = await WriterRepository.get_by_id(session, id)
        if not writer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Writer not found")
        return WriterResponseTo(**writer.__dict__)

    @staticmethod
    async def get_all(session, skip=0, limit=10) -> list[WriterResponseTo]:
        writers = await WriterRepository.get_all(session, skip, limit)
        return [WriterResponseTo(**w.__dict__) for w in writers]

    @staticmethod
    async def update(session, id: int, dto: WriterRequestTo) -> WriterResponseTo:
        updated = await WriterRepository.update(session, id, dto.dict())
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Writer not found")
        return WriterResponseTo(**updated.__dict__)

    @staticmethod
    async def delete(session, id: int):
        deleted = await WriterRepository.delete(session, id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Writer not found")

    @staticmethod
    async def get_by_news_id(session, news_id: int) -> WriterResponseTo:
        news = await NewsRepository.get_by_id(session, news_id)
        if not news:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
        writer = await WriterRepository.get_by_id(session, news.writer_id)
        if not writer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Writer not found")
        return WriterResponseTo(**writer.__dict__)

# Сервис для News
class NewsService:
    @staticmethod
    async def create(session, dto: NewsRequestTo) -> NewsResponseTo:
        news = News(**dto.dict())
        news = await NewsRepository.create(session, news)
        return NewsResponseTo(**news.__dict__)

    @staticmethod
    async def get_by_id(session, id: int) -> NewsResponseTo:
        news = await NewsRepository.get_by_id(session, id)
        if not news:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
        return NewsResponseTo(**news.__dict__)

    @staticmethod
    async def get_all(session, skip=0, limit=10, sort_by="id", sort_order="asc", title=None):
        query = select(News)
        if title:
            query = query.where(News.title.ilike(f"%{title}%"))
        if sort_order == "desc":
            query = query.order_by(desc(getattr(News, sort_by)))
        else:
            query = query.order_by(asc(getattr(News, sort_by)))
        result = await session.execute(query.offset(skip).limit(limit))
        news_list = result.scalars().all()
        return [NewsResponseTo(**n.__dict__) for n in news_list]

    @staticmethod
    async def update(session, id: int, dto: NewsRequestTo) -> NewsResponseTo:
        updated = await NewsRepository.update(session, id, dto.dict())
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
        return NewsResponseTo(**updated.__dict__)

    @staticmethod
    async def delete(session, id: int):
        deleted = await NewsRepository.delete(session, id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")

# Сервис для Label
class LabelService:
    @staticmethod
    async def create(session, dto: LabelRequestTo) -> LabelResponseTo:
        label = Label(**dto.dict())
        label = await LabelRepository.create(session, label)
        return LabelResponseTo(**label.__dict__)

    @staticmethod
    async def get_by_id(session, id: int) -> LabelResponseTo:
        label = await LabelRepository.get_by_id(session, id)
        if not label:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
        return LabelResponseTo(**label.__dict__)

    @staticmethod
    async def get_all(session, skip=0, limit=10) -> list[LabelResponseTo]:
        labels = await LabelRepository.get_all(session, skip, limit)
        return [LabelResponseTo(**l.__dict__) for l in labels]

    @staticmethod
    async def update(session, id: int, dto: LabelRequestTo) -> LabelResponseTo:
        updated = await LabelRepository.update(session, id, dto.dict())
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
        return LabelResponseTo(**updated.__dict__)

    @staticmethod
    async def delete(session, id: int):
        deleted = await LabelRepository.delete(session, id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")

# Сервис для Message
class MessageService:
    @staticmethod
    async def create(session, dto: MessageRequestTo) -> MessageResponseTo:
        message = Message(**dto.dict())
        message = await MessageRepository.create(session, message)
        return MessageResponseTo(**message.__dict__)

    @staticmethod
    async def get_by_id(session, id: int) -> MessageResponseTo:
        message = await MessageRepository.get_by_id(session, id)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        return MessageResponseTo(**message.__dict__)

    @staticmethod
    async def get_all(session, skip=0, limit=10) -> list[MessageResponseTo]:
        messages = await MessageRepository.get_all(session, skip, limit)
        return [MessageResponseTo(**m.__dict__) for m in messages]

    @staticmethod
    async def update(session, id: int, dto: MessageRequestTo) -> MessageResponseTo:
        updated = await MessageRepository.update(session, id, dto.dict())
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        return MessageResponseTo(**updated.__dict__)

    @staticmethod
    async def delete(session, id: int):
        deleted = await MessageRepository.delete(session, id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")