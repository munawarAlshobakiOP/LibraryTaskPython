from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """
    Base model for User, shared by create and update operations.
    """

    username: str = Field(...)


class UserCreate(UserBase):
    """
    Model for creating a new user.
    """

    password: str = Field(...)


class User(UserBase):
    """
    Model representing a user with an ID.
    """

    created_at: datetime = Field(...)
    id: UUID = Field(...)

    class Config:
        """
        Configuration for the User model.
        """

        from_attributes = True
        populate_by_name = True
