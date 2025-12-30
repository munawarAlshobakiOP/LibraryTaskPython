from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repositories.borrower_repository_impl import SQLBorrowerRepository
from app.repositories.loan_repository_impl import SQLLoanRepository
from app.schemas.borrower import BorrowerCreate, BorrowerUpdate
from app.services.borrower_service import BorrowerService

router = APIRouter(prefix="/borrowers", tags=["borrowers"])


def borrower_loader(db: Session = Depends(get_db)) -> BorrowerService:
    """
    Get an instance of the BorrowerService with a database session.
    Args:
        db (Session): The database session.
    Returns:
        BorrowerService: An instance of BorrowerService.
    """
    return BorrowerService(SQLBorrowerRepository(db), SQLLoanRepository(db))


@router.get("/")
def list_borrowers(svc: BorrowerService = Depends(borrower_loader)):
    """
    List all borrowers.
    Returns:
        A list of all borrowers.
    """
    return svc.get_borrowers()


@router.get("/{id}")
def get_borrower(id: str, svc: BorrowerService = Depends(borrower_loader)):
    """
    Get a borrower by their ID.
    Args:
        id (str): The ID of the borrower.
        svc (BorrowerService): The borrower service instance.
    Returns:
        The Borrower object if found, otherwise None.
    """
    return svc.get_borrower_by_id(id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_new_borrower(
    data: BorrowerCreate, svc: BorrowerService = Depends(borrower_loader)
):
    """
    Add a new borrower.
    Args:
        data (BorrowerCreate): The borrower data to create.
        svc (BorrowerService): The borrower service instance.
    Returns:
        The created borrower.
    """
    return svc.create_borrower(data)


@router.put("/{id}")
def modify_borrower(
    id: str, data: BorrowerUpdate, svc: BorrowerService = Depends(borrower_loader)
):
    """
    Update a borrower's information.
    """
    return svc.update_borrower(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_borrower(id: str, svc: BorrowerService = Depends(borrower_loader)):
    """
    Remove a borrower.
    Args:
        id (str): The ID of the borrower to delete.
        svc (BorrowerService): The borrower service instance.

    """
    svc.delete_borrower(id)


@router.get("/{id}/loans")
def get_borrower_loans(id: str, svc: BorrowerService = Depends(borrower_loader)):
    """
    Get a borrower's profile along with their loans.
    """
    return svc.get_borrower_profile_with_loans(id)
