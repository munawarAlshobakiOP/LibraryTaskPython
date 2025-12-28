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
    Args:
        svc (BorrowerService): The borrower service instance.
    Returns:
        A list of all borrowers.
    """
    return svc.get_borrowers()


@router.get("/{id}")
def get_profile(id: str, svc: BorrowerService = Depends(borrower_loader)):
    """
    Get the profile of a specific borrower along with their loans.
    Args:
        id (str): The ID of the borrower.
        svc (BorrowerService): The borrower service instance.
    Returns:
        The borrower's profile with their loans.
    """
    return svc.get_borrower_profile_with_loans(id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_new_user(data: BorrowerCreate, svc: BorrowerService = Depends(borrower_loader)):
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
def update_user_info(
    id: str, data: BorrowerUpdate, svc: BorrowerService = Depends(borrower_loader)
):
    """
    Update a borrower's information.
    Args:
        id (str): The ID of the borrower.
        data (BorrowerUpdate): The updated borrower data.
        svc (BorrowerService): The borrower service instance.
    Returns:
        The updated borrower.
    """
    return svc.update_borrower(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(id: str, svc: BorrowerService = Depends(borrower_loader)):
    """
    Remove a borrower.
    Args:
        id (str): The ID of the borrower to delete.
        svc (BorrowerService): The borrower service instance.
    Returns:
        None.
    """
    svc.delete_borrower(id)
