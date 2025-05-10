from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# Связь многие-ко-многим между Topic и Mark
topic_mark = Table(
    'tbl_topic_mark',
    Base.metadata,
    Column('topic_id', Integer, ForeignKey('tbl_topic.id'), primary_key=True),
    Column('mark_id', Integer, ForeignKey('tbl_mark.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'tbl_user'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    
    topics = relationship("Topic", back_populates="user", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = 'tbl_topic'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('tbl_user.id'), nullable=False)
    
    user = relationship("User", back_populates="topics")
    messages = relationship("Message", back_populates="topic", cascade="all, delete-orphan")
    marks = relationship("Mark", secondary=topic_mark, back_populates="topics")

class Message(Base):
    __tablename__ = 'tbl_message'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    topic_id = Column(Integer, ForeignKey('tbl_topic.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    topic = relationship("Topic", back_populates="messages")

class Mark(Base):
    __tablename__ = 'tbl_mark'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    topics = relationship("Topic", secondary=topic_mark, back_populates="marks")