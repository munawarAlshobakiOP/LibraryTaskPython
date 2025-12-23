from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.loan import LoanCreate
from app.services.loan_service import LoanService
from app.repositories.loan_repository_impl import SQLLoanRepository
from app.core.dependencies import get_db

router = APIRouter(prefix="/loans", tags=["Loans"])


def get_service_instance(db: Session = Depends(get_db)):
    return LoanService(SQLLoanRepository(db))


@router.post("/")
def create_new_loan(
    payload: LoanCreate, svc: LoanService = Depends(get_service_instance)
):
    return svc.create_loan(payload)


@router.get("/active")
def list_active(svc: LoanService = Depends(get_service_instance)):
    return svc.get_active_loans()


@router.put("/{id}/return")
def handle_return(id: UUID, svc: LoanService = Depends(get_service_instance)):
    return svc.return_loan(str(id))


@router.get("/history/borrower/{id}")
def user_loan_history(id: str, svc: LoanService = Depends(get_service_instance)):
    return svc.get_borrower_loan_history(id)
