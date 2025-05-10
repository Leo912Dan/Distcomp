from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

class MessageBase(BaseModel):
    content: str
    topic_id: UUID4
    user_id: UUID4

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: Optional[str] = None

class Message(MessageBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 