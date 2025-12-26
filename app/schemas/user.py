from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., alias="Username")


class UserCreate(UserBase):
    password: str = Field(..., alias="Password")


class User(UserBase):
    id: UUID = Field(..., alias="Id")
    created_at: datetime = Field(..., alias="CreatedAt")

    class Config:
        from_attributes = True
        populate_by_name = True
