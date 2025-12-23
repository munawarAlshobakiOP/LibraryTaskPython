from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class BookBase(BaseModel):
    title: str = Field(alias="Title")
    isbn: str = Field(alias="ISBN")
    published_date: str = Field(alias="PublishedDate")
    author_id: UUID = Field(alias="AuthorId")


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, alias="Title")
    isbn: Optional[str] = Field(None, alias="ISBN")
    published_date: Optional[str] = Field(None, alias="PublishedDate")
    author_id: Optional[UUID] = Field(None, alias="AuthorId")


class Book(BookBase):
    id: UUID = Field(alias="Id")
    author_name: Optional[str] = Field(None, alias="AuthorName")

    class Config:
        from_attributes = True
        populate_by_name = True
