from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """
    Base model for Book, shared by create and update operations.
    """

    author_id: UUID = Field()
    isbn: str = Field()
    published_date: date = Field()
    title: str = Field()


class BookCreate(BookBase):
    """
    Model for creating a new book.
    """

    pass


class BookUpdate(BaseModel):
    """
    Model for updating an existing book.
    """

    author_id: Optional[UUID] = Field(None)
    isbn: Optional[str] = Field(None)
    published_date: Optional[date] = Field(None)
    title: Optional[str] = Field(None)


class Book(BookBase):
    """
    Model representing a book with an ID.
    """

    author_name: Optional[str] = Field(None)
    id: UUID = Field()

    class Config:
        """
        Configuration for the Book model.
        """

        from_attributes = True
        populate_by_name = True
