from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.config.kafka import MESSAGE_STATES

class MessageBase(BaseModel):
    content: str
    topic_id: int
    user_id: int
    state: str = MESSAGE_STATES["PENDING"]

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: Optional[str] = None
    state: Optional[str] = None

class Message(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 