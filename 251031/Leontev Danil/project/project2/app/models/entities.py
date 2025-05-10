from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

# Таблица для связи многие-ко-многим между Topic и Mark
topic_mark = Table(
    'tbl_topic_mark',
    Base.metadata,
    Column('topic_id', Integer, ForeignKey('tbl_topic.id')),
    Column('mark_id', Integer, ForeignKey('tbl_mark.id'))
)

class User(Base):
    __tablename__ = 'tbl_user'
    
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    topics = relationship("Topic", back_populates="user")

class Topic(Base):
    __tablename__ = 'tbl_topic'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('tbl_user.id'))
    user = relationship("User", back_populates="topics")
    messages = relationship("Message", back_populates="topic")
    marks = relationship("Mark", secondary=topic_mark, back_populates="topics")

class Mark(Base):
    __tablename__ = 'tbl_mark'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    topics = relationship("Topic", secondary=topic_mark, back_populates="marks")

class Message(Base):
    __tablename__ = 'tbl_message'
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created = Column(DateTime, default=datetime.utcnow)
    topic_id = Column(Integer, ForeignKey('tbl_topic.id'))
    topic = relationship("Topic", back_populates="messages") 