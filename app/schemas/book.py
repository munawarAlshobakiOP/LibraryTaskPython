from datetime import date
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class BookBase(BaseModel):
    title: str = Field()
    isbn: str = Field()
    published_date: date = Field()
    author_id: UUID = Field()


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None)
    isbn: Optional[str] = Field(None)
    published_date: Optional[date] = Field(None)
    author_id: Optional[UUID] = Field(None)


class Book(BookBase):
    id: UUID = Field()
    author_name: Optional[str] = Field(None)

    class Config:
        from_attributes = True
        populate_by_name = True
