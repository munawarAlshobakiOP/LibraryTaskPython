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
        payload (LoanCreate): The loan data to create.
        svc (LoanService): The loan service instance.
    Returns:
        The created loan.
    """
    return svc.create_loan(payload)


@router.get("/active")
def list_active(svc: LoanService = Depends(get_service_instance)):
    """
    List all active loans.
    Args:
        svc (LoanService): The loan service instance.
    Returns:
        A list of active loans.
    """
    return svc.get_active_loans()


@router.put("/{id}/return")
def handle_return(id: UUID, svc: LoanService = Depends(get_service_instance)):
    """
    Return a loan by its ID.
    Args:
        id (UUID): The ID of the loan to return.
        svc (LoanService): The loan service instance.
    Returns:
        The updated loan after return.
    """
    return svc.return_loan(str(id))


@router.get("/history/borrower/{id}")
def user_loan_history(id: str, svc: LoanService = Depends(get_service_instance)):
    """
    Get the loan history for a specific borrower.
    Args:
        id (str): The ID of the borrower.
        svc (LoanService): The loan service instance.
    Returns:
        A list of loans for the specified borrower.
    """
    return svc.get_borrower_loan_history(id)
