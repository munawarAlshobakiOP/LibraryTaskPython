from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.repositories.author_repository_impl import SQLAuthorRepository
from app.repositories.loan_repository_impl import SQLLoanRepository
from app.repositories.book_repository_impl import SQLBookRepository
from app.core.dependencies import get_db
from app.schemas.book import BookCreate, BookUpdate
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])


def get_svc(db: Session = Depends(get_db)) -> BookService:
    return BookService(
        SQLBookRepository(db), SQLAuthorRepository(db), SQLLoanRepository(db)
    )


@router.get("/")
def list_books(svc: BookService = Depends(get_svc)):
    return svc.get_books()


@router.get("/{id}")
def get_book(id: str, svc: BookService = Depends(get_svc)):
    return svc.get_book_by_id(id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_new_book(data: BookCreate, svc: BookService = Depends(get_svc)):
    return svc.create_book(data)


@router.put("/{id}")
def modify_book(id: str, data: BookUpdate, svc: BookService = Depends(get_svc)):
    return svc.update_book(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_book(id: str, svc: BookService = Depends(get_svc)):
    svc.delete_book(id)
