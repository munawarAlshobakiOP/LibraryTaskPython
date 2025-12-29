from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    """
    Base model for Author, shared by create and update operations.
    """

    bio: Optional[str] = Field(None)
    name: str = Field()


class AuthorCreate(AuthorBase):
    """
    Model for creating a new author.
    """

    pass


class AuthorUpdate(BaseModel):
    """
    Model for updating an existing author.
    """

    bio: Optional[str] = Field(None)
    name: Optional[str] = Field(None)


class Author(AuthorBase):
    """
    Model representing an author with an ID.
    """

    id: UUID = Field()

    class Config:
        """
        Configuration for the Author model.
        """

        from_attributes = True
        populate_by_name = True
