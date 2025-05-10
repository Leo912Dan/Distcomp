from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    login: str
    password: str
    firstname: str
    lastname: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    login: Optional[str] = None
    password: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 