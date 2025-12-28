from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(...)


class UserCreate(UserBase):
    password: str = Field(...)


class User(UserBase):
    id: UUID = Field(...)
    created_at: datetime = Field(...)

    class Config:
        from_attributes = True
        populate_by_name = True
