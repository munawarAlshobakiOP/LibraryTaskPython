from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repositories.loan_repository_impl import SQLLoanRepository
from app.schemas.loan import LoanCreate
from app.services.loan_service import LoanService

router = APIRouter(prefix="/loans", tags=["Loans"])


def get_service_instance(db: Session = Depends(get_db)):
    """
    Get an instance of the LoanService with a database session.
    Args:
        db (Session): The database session.
    Returns:
        LoanService: An instance of LoanService.
    """
    return LoanService(SQLLoanRepository(db))


@router.post("/")
def create_new_loan(
    payload: LoanCreate, svc: LoanService = Depends(get_service_instance)
):
    """
    Create a new loan.
    Args:
        payload (LoanCreate): The data for creating a new loan.
        svc (LoanService): The loan service instance.
    Returns:
        The created loan.
    """
    return svc.create_loan(payload)


@router.get("/active")
def list_active_loans(svc: LoanService = Depends(get_service_instance)):
    """
    List all active loans.
    Args:
        svc (LoanService): The loan service instance.
    Returns:
        A list of active loans.
    """
    return svc.get_active_loans()


@router.get("/history/{borrower_id}")
def get_borrower_history(
    borrower_id: str, svc: LoanService = Depends(get_service_instance)
):
    """
    Get the loan history for a specific borrower.
    Args:
        borrower_id (str): The ID of the borrower.
        svc (LoanService): The loan service instance.
    Returns:
        A list of loans for the borrower.
    """
    return svc.get_borrower_loan_history(borrower_id)


@router.post("/{loan_id}/return")
def return_book(loan_id: str, svc: LoanService = Depends(get_service_instance)):
    """
    Return a loaned book.
    Args:
        loan_id (str): The ID of the loan to return.
        svc (LoanService): The loan service instance.
    Returns:
        The updated loan.
    """
    return svc.return_loan(loan_id)
