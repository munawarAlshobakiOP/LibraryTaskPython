from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class LoanBase(BaseModel):
    book_id: UUID = Field(alias="BookId")
    borrower_id: UUID = Field(alias="BorrowerId")


class LoanCreate(LoanBase):
    loan_date: Optional[str] = Field(None, alias="LoanDate")
    return_date: Optional[str] = Field(None, alias="ReturnDate")


class LoanUpdate(LoanBase):
    loan_date: Optional[str] = Field(None, alias="LoanDate")
    return_date: Optional[str] = Field(None, alias="ReturnDate")


class Loan(LoanBase):
    id: UUID = Field(alias="Id")
    loan_date: Optional[datetime] = Field(None, alias="LoanDate")
    return_date: Optional[datetime] = Field(None, alias="ReturnDate")

    class Config:
        from_attributes = True
        populate_by_name = True
