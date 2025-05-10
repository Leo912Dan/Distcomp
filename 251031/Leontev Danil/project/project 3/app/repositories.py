from typing import Dict, Generic, TypeVar, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from app.models import Message, User, Topic, Mark

T = TypeVar('T')

class UserRepository:
    @staticmethod
    def create(db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, user_id: int, user_data: dict) -> Optional[User]:
        user = UserRepository.get_by_id(db, user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        user = UserRepository.get_by_id(db, user_id)
        if user:
            db.delete(user)
            db.commit()
            return True
        return False

class TopicRepository:
    @staticmethod
    def create(db: Session, topic: Topic) -> Topic:
        db.add(topic)
        db.commit()
        db.refresh(topic)
        return topic

    @staticmethod
    def get_by_id(db: Session, topic_id: int) -> Optional[Topic]:
        return db.query(Topic).filter(Topic.id == topic_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10) -> List[Topic]:
        return db.query(Topic).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[Topic]:
        return db.query(Topic).filter(Topic.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, topic_id: int, topic_data: dict) -> Optional[Topic]:
        topic = TopicRepository.get_by_id(db, topic_id)
        if topic:
            for key, value in topic_data.items():
                setattr(topic, key, value)
            db.commit()
            db.refresh(topic)
        return topic

    @staticmethod
    def delete(db: Session, topic_id: int) -> bool:
        topic = TopicRepository.get_by_id(db, topic_id)
        if topic:
            db.delete(topic)
            db.commit()
            return True
        return False

class MarkRepository:
    @staticmethod
    def create(db: Session, mark: Mark) -> Mark:
        db.add(mark)
        db.commit()
        db.refresh(mark)
        return mark

    @staticmethod
    def get_by_id(db: Session, mark_id: int) -> Optional[Mark]:
        return db.query(Mark).filter(Mark.id == mark_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10) -> List[Mark]:
        return db.query(Mark).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, mark_id: int, mark_data: dict) -> Optional[Mark]:
        mark = MarkRepository.get_by_id(db, mark_id)
        if mark:
            for key, value in mark_data.items():
                setattr(mark, key, value)
            db.commit()
            db.refresh(mark)
        return mark

    @staticmethod
    def delete(db: Session, mark_id: int) -> bool:
        mark = MarkRepository.get_by_id(db, mark_id)
        if mark:
            db.delete(mark)
            db.commit()
            return True
        return False

class MessageRepository:
    @staticmethod
    def create(db: Session, message: Message) -> Message:
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def get_by_id(db: Session, message_id: int) -> Optional[Message]:
        return db.query(Message).filter(Message.id == message_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10) -> List[Message]:
        return db.query(Message).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_topic_id(db: Session, topic_id: int, skip: int = 0, limit: int = 10) -> List[Message]:
        return db.query(Message).filter(Message.topic_id == topic_id).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, message_id: int, message_data: dict) -> Optional[Message]:
        message = MessageRepository.get_by_id(db, message_id)
        if message:
            for key, value in message_data.items():
                setattr(message, key, value)
            db.commit()
            db.refresh(message)
        return message

    @staticmethod
    def delete(db: Session, message_id: int) -> bool:
        message = MessageRepository.get_by_id(db, message_id)
        if message:
            db.delete(message)
            db.commit()
            return True
        return False