from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class LoanBase(BaseModel):
    book_id: UUID = Field()
    borrower_id: UUID = Field()


class LoanCreate(LoanBase):
    loan_date: Optional[str] = Field(None)
    return_date: Optional[str] = Field(None)


class LoanUpdate(LoanBase):
    loan_date: Optional[str] = Field(None)
    return_date: Optional[str] = Field(None)


class Loan(LoanBase):
    id: UUID = Field()
    loan_date: Optional[datetime] = Field(None)
    return_date: Optional[datetime] = Field(None)

    class Config:
        from_attributes = True
        populate_by_name = True
