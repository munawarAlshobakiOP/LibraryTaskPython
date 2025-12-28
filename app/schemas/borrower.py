from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional
from uuid import UUID

PHONE_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")


class BorrowerBase(BaseModel):
    name: str = Field()
    email: str = Field()
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
    pass


class BorrowerUpdate(BorrowerBase):
    name: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)


class Borrower(BorrowerBase):
    id: UUID = Field()

    class Config:
        from_attributes = True
        populate_by_name = True
