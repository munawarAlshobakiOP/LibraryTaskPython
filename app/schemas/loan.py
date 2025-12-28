from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class LoanBase(BaseModel):
    """
    Base model for Loan, shared by create and update operations.
    """

    borrower_id: UUID = Field()
    book_id: UUID = Field()


class LoanCreate(LoanBase):
    """
    Model for creating a new loan.
    """

    loan_date: Optional[str] = Field(None)
    return_date: Optional[str] = Field(None)


class LoanUpdate(LoanBase):
    """
    Model for updating an existing loan.
    """

    loan_date: Optional[str] = Field(None)
    return_date: Optional[str] = Field(None)


class Loan(LoanBase):
    """
    Model representing a loan with an ID.
    """

    id: UUID = Field()
    loan_date: Optional[datetime] = Field(None)
    return_date: Optional[datetime] = Field(None)

    class Config:
        """
        Configuration for the Loan model.
        """

        from_attributes = True
        populate_by_name = True
