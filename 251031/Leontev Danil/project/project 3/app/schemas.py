from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    login: str
    firstname: str
    lastname: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class TopicBase(BaseModel):
    name: str
    user_id: int
    mark_ids: Optional[List[int]] = None

class TopicCreate(TopicBase):
    pass

class Topic(TopicBase):
    id: int
    
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str
    topic_id: int

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MarkBase(BaseModel):
    name: str

class MarkCreate(MarkBase):
    pass

class Mark(MarkBase):
    id: int
    
    class Config:
        from_attributes = True
