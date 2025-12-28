from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class AuthorBase(BaseModel):
    name: str = Field()
    bio: Optional[str] = Field(None)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None)
    bio: Optional[str] = Field(None)


class Author(AuthorBase):
    id: UUID = Field()

    class Config:
        from_attributes = True
        populate_by_name = True
