from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.author import AuthorCreate, AuthorUpdate
from app.services.author_service import AuthorService
from app.repositories.author_repository_impl import SQLAuthorRepository
from app.repositories.book_repository_impl import SQLBookRepository

router = APIRouter(prefix="/authors", tags=["authors"])


def author_svc_helper(db: Session = Depends(get_db)) -> AuthorService:
    return AuthorService(SQLAuthorRepository(db), SQLBookRepository(db))


@router.get("/")
def list_all_authors(svc: AuthorService = Depends(author_svc_helper)):
    return svc.get_authors()


@router.get("/{id}")
def get_author_profile(id: str, svc: AuthorService = Depends(author_svc_helper)):
    return svc.get_author_by_id(id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_author(req: AuthorCreate, svc: AuthorService = Depends(author_svc_helper)):
    return svc.create_author(req)


@router.put("/{id}")
def edit_author(
    id: str, req: AuthorUpdate, svc: AuthorService = Depends(author_svc_helper)
):
    return svc.update_author(id, req)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_author(id: str, svc: AuthorService = Depends(author_svc_helper)):
    svc.delete_author(id)
