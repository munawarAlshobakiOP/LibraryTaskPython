from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.borrower import BorrowerCreate, BorrowerUpdate
from app.services.borrower_service import BorrowerService
from app.repositories.borrower_repository_impl import SQLBorrowerRepository
from app.repositories.loan_repository_impl import SQLLoanRepository

router = APIRouter(prefix="/borrowers", tags=["borrowers"])


def borrower_loader(db: Session = Depends(get_db)) -> BorrowerService:
    return BorrowerService(SQLBorrowerRepository(db), SQLLoanRepository(db))


@router.get("/")
def list_borrowers(svc: BorrowerService = Depends(borrower_loader)):
    return svc.get_borrowers()


@router.get("/{id}")
def get_profile(id: str, svc: BorrowerService = Depends(borrower_loader)):
    return svc.get_borrower_profile_with_loans(id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_new_user(data: BorrowerCreate, svc: BorrowerService = Depends(borrower_loader)):
    return svc.create_borrower(data)


@router.put("/{id}")
def update_user_info(
    id: str, data: BorrowerUpdate, svc: BorrowerService = Depends(borrower_loader)
):
    return svc.update_borrower(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(id: str, svc: BorrowerService = Depends(borrower_loader)):
    svc.delete_borrower(id)
