from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.repositories import UserRepository, TopicRepository, MessageRepository, MarkRepository
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .discussion.init_cassandra import wait_for_cassandra
from .discussion.router import router as discussion_router

app = FastAPI(title="Entities API", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

# Инициализация Cassandra
@app.on_event("startup")
async def startup_event():
    wait_for_cassandra()

# Подключаем роутеры
app.include_router(discussion_router)

# User endpoints
@app.post("/api/v1.0/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    return UserRepository.create(db, db_user)

@app.get("/api/v1.0/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/v1.0/users/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return UserRepository.get_all(db, skip, limit)

@app.put("/api/v1.0/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated_user = UserRepository.update(db, user_id, user.model_dump())
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/api/v1.0/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not UserRepository.delete(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

# Topic endpoints
@app.post("/api/v1.0/topics/", response_model=schemas.Topic)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    db_topic = models.Topic(**topic.model_dump(exclude={'mark_ids'}))
    if topic.mark_ids:
        marks = [MarkRepository.get_by_id(db, mark_id) for mark_id in topic.mark_ids]
        db_topic.marks = [mark for mark in marks if mark]
    return TopicRepository.create(db, db_topic)

@app.get("/api/v1.0/topics/{topic_id}", response_model=schemas.Topic)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = TopicRepository.get_by_id(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@app.get("/api/v1.0/topics/", response_model=List[schemas.Topic])
def get_topics(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return TopicRepository.get_all(db, skip, limit)

@app.get("/api/v1.0/topics/user/{user_id}", response_model=List[schemas.Topic])
def get_user_topics(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return TopicRepository.get_by_user_id(db, user_id, skip, limit)

@app.put("/api/v1.0/topics/{topic_id}", response_model=schemas.Topic)
def update_topic(topic_id: int, topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    updated_topic = TopicRepository.update(db, topic_id, topic.model_dump(exclude={'mark_ids'}))
    if not updated_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    if topic.mark_ids:
        marks = [MarkRepository.get_by_id(db, mark_id) for mark_id in topic.mark_ids]
        updated_topic.marks = [mark for mark in marks if mark]
        db.commit()
    return updated_topic

@app.delete("/api/v1.0/topics/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    if not TopicRepository.delete(db, topic_id):
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"message": "Topic deleted"}

# Message endpoints
@app.post("/api/v1.0/messages/", response_model=schemas.Message)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_message = models.Message(**message.model_dump())
    return MessageRepository.create(db, db_message)

@app.get("/api/v1.0/messages/{message_id}", response_model=schemas.Message)
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = MessageRepository.get_by_id(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@app.get("/api/v1.0/messages/", response_model=List[schemas.Message])
def get_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return MessageRepository.get_all(db, skip, limit)

@app.get("/api/v1.0/messages/topic/{topic_id}", response_model=List[schemas.Message])
def get_topic_messages(topic_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return MessageRepository.get_by_topic_id(db, topic_id, skip, limit)

@app.put("/api/v1.0/messages/{message_id}", response_model=schemas.Message)
def update_message(message_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db)):
    updated_message = MessageRepository.update(db, message_id, message.model_dump())
    if not updated_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated_message

@app.delete("/api/v1.0/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    if not MessageRepository.delete(db, message_id):
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted"}

# Mark endpoints
@app.post("/api/v1.0/marks/", response_model=schemas.Mark)
def create_mark(mark: schemas.MarkCreate, db: Session = Depends(get_db)):
    db_mark = models.Mark(**mark.model_dump())
    return MarkRepository.create(db, db_mark)

@app.get("/api/v1.0/marks/{mark_id}", response_model=schemas.Mark)
def get_mark(mark_id: int, db: Session = Depends(get_db)):
    mark = MarkRepository.get_by_id(db, mark_id)
    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found")
    return mark

@app.get("/api/v1.0/marks/", response_model=List[schemas.Mark])
def get_marks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return MarkRepository.get_all(db, skip, limit)

@app.put("/api/v1.0/marks/{mark_id}", response_model=schemas.Mark)
def update_mark(mark_id: int, mark: schemas.MarkCreate, db: Session = Depends(get_db)):
    updated_mark = MarkRepository.update(db, mark_id, mark.model_dump())
    if not updated_mark:
        raise HTTPException(status_code=404, detail="Mark not found")
    return updated_mark

@app.delete("/api/v1.0/marks/{mark_id}")
def delete_mark(mark_id: int, db: Session = Depends(get_db)):
    if not MarkRepository.delete(db, mark_id):
        raise HTTPException(status_code=404, detail="Mark not found")
    return {"message": "Mark deleted"}

@app.get("/")
async def root():
    return {"message": "Welcome to Discussion API"}