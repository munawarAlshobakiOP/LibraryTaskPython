import re
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


PHONE_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")


class BorrowerBase(BaseModel):
    """
    Base model for Borrower, shared by create and update operations.
    """

    email: str = Field()
    name: str = Field()
    phone: str = Field()

    @field_validator("phone")
    @classmethod
    def validate_and_normalize_phone(cls, value: str) -> str:
        normalized = re.sub(r"[^\d+]", "", value)

        if not PHONE_REGEX.match(normalized):
            raise ValueError(
                "Invalid phone number format. Expected E.164 (e.g., +1234567890)."
            )

        return normalized


class BorrowerCreate(BorrowerBase):
    """
    Model for creating a new borrower.
    """

    pass


class BorrowerUpdate(BorrowerBase):
    """
    Model for updating an existing borrower.
    """

    email: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)


class Borrower(BorrowerBase):
    """
    Model representing a borrower with an ID.
    """

    id: UUID = Field()

    class Config:
        """
        Configuration for the Borrower model.
        """

        from_attributes = True
        populate_by_name = True
