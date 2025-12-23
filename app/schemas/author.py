from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class AuthorBase(BaseModel):
    name: str = Field(alias="Name")
    bio: Optional[str] = Field(None, alias="Bio")


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, alias="Name")
    bio: Optional[str] = Field(None, alias="Bio")


class Author(AuthorBase):
    id: UUID = Field(alias="Id")

    class Config:
        from_attributes = True
        populate_by_name = True
