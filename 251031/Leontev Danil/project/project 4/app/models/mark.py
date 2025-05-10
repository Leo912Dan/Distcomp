from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MarkBase(BaseModel):
    name: str

class MarkCreate(MarkBase):
    pass

class MarkUpdate(BaseModel):
    name: Optional[str] = None

class Mark(MarkBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 