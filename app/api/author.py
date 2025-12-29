from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repositories.author_repository_impl import SQLAuthorRepository
from app.repositories.book_repository_impl import SQLBookRepository
from app.schemas.author import AuthorCreate, AuthorUpdate
from app.services.author_service import AuthorService

router = APIRouter(prefix="/authors", tags=["authors"])


def author_svc_helper(db: Session = Depends(get_db)) -> AuthorService:
    """
    Get an instance of the AuthorService with a database session.
    Args:
        db (Session): The database session.
    Returns:
        AuthorService: An instance of AuthorService.
    """
    return AuthorService(SQLAuthorRepository(db), SQLBookRepository(db))


@router.get("/")
def list_all_authors(svc: AuthorService = Depends(author_svc_helper)):
    """
    List all authors.
    Returns:
        A list of all authors.
    """
    return svc.get_authors()


@router.get("/{id}")
def get_author_profile(id: str, svc: AuthorService = Depends(author_svc_helper)):
    """
    Get an author by their ID.
    Args:
        id (str): The ID of the author.
        svc (AuthorService): The author service instance.
    Returns:
        The Author object if found, otherwise None.
    """
    return svc.get_author_by_id(id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_author(req: AuthorCreate, svc: AuthorService = Depends(author_svc_helper)):
    """
    Add a new author.
    Args:
        req (AuthorCreate): The author data to create.
        svc (AuthorService): The author service instance.
    Returns:
        The created author.
    """
    return svc.create_author(req)


@router.put("/{id}")
def edit_author(
    id: str, req: AuthorUpdate, svc: AuthorService = Depends(author_svc_helper)
):
    """
    Update an author's information.
    Args:
        id (str): The ID of the author.
        req (AuthorUpdate): The updated author data.
        svc (AuthorService): The author service instance.
    Returns:
        The updated author.
    """
    return svc.update_author(id, req)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_author(id: str, svc: AuthorService = Depends(author_svc_helper)):
    """
    Remove an author.
    Args:
        id (str): The ID of the author to delete.
        svc (AuthorService): The author service instance.
    """
    svc.delete_author(id)
