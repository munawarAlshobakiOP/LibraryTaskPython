from datetime import datetime
from uuid import uuid4
from typing import Optional

from app.core.exceptions import NotFoundException
from app.models.author import Author as AuthorModel
from app.repositories.author_repository import AuthorRepositoryInterface
from app.repositories.book_repository import BookRepositoryInterface
from app.schemas.author import AuthorCreate, AuthorUpdate, Author as AuthorSchema
from app.schemas.book import Book as BookSchema
from app.domain.entities.author import AuthorCreated, AuthorUpdated, AuthorDeleted
from app.core.events import publish_domain_event


class AuthorService:
    def __init__(
        self,
        author_repo: AuthorRepositoryInterface,
        book_repo: BookRepositoryInterface,
    ):
        """
        Initialize the AuthorService with the given repositories.
        """
        self.author_repo = author_repo
        self.book_repo = book_repo

    def create_author(self, data: AuthorCreate):
        """
        Create a new author.
        """
        obj = AuthorModel(name=data.name, bio=data.bio)
        res = self.author_repo.create_author(obj)

        schema_data = AuthorSchema.model_validate(res)
        event = AuthorCreated(
            aggregate_id=res.id,
            data=schema_data.model_dump(mode="json"),
        )

        publish_domain_event(event)

        return schema_data

    def get_author_by_id(self, auth_id: str):
        """
        Retrieve an author by their ID.
        """
        author = self.author_repo.get_author_by_id(auth_id)

        if not author:
            raise NotFoundException("Author not found")

        books = self.book_repo.get_books_by_author_id(auth_id)
        blist = []
        for b in books:
            book_schema = BookSchema.model_validate(b)
            book_schema.author_name = author.name
            blist.append(book_schema)

        return {
            "author": AuthorSchema.model_validate(author),
            "books": blist,
        }

    def get_authors(self):
        """
        Retrieve all authors.
        """
        records = self.author_repo.get_authors()

        if not records:
            raise NotFoundException("No authors found")

        result = []
        for r in records:
            result.append(AuthorSchema.model_validate(r))
        return result

    def update_author(self, aid: str, data: AuthorUpdate):
        """
        Update an existing author.
        """
        author = self.author_repo.get_author_by_id(aid)

        if author is None:
            raise NotFoundException("Author not found")

        if data.name is not None:
            author.name = data.name

        if data.bio is not None:
            author.bio = data.bio

        updated = self.author_repo.update_author(author)

        schema_data = AuthorSchema.model_validate(updated)
        event = AuthorUpdated(
            aggregate_id=updated.id,
            data=schema_data.model_dump(mode="json"),
        )

        publish_domain_event(event)

        return schema_data

    def delete_author(self, aid: str):
        """
        Delete an author by their ID.
        """
        author = self.author_repo.get_author_by_id(aid)
        if not author:
            raise NotFoundException("Author not found")

        event = AuthorDeleted(
            aggregate_id=author.id,
            data=AuthorSchema.model_validate(author).model_dump(mode="json"),
        )

        self.author_repo.delete_author(aid)

        publish_domain_event(event)
