from datetime import datetime
from uuid import uuid4
from typing import Optional

from app.core.exceptions import ActiveLoanExistsException, NotFoundException
from app.models.book import Book as BookModel
from app.repositories.author_repository import AuthorRepositoryInterface
from app.repositories.book_repository import BookRepositoryInterface
from app.repositories.loan_repository import LoanRepositoryInterface
from app.schemas.book import BookCreate, BookUpdate, Book as BookSchema
from app.schemas.domain_event import BookCreated, BookUpdated, BookDeleted
from app.core.events import publish_domain_event


class BookService:
    def __init__(
        self,
        book_repo: BookRepositoryInterface,
        author_repo: AuthorRepositoryInterface,
        loan_repo: LoanRepositoryInterface,
    ):
        """
        Initialize the BookService with the given repositories.
        """
        self.book_repo = book_repo
        self.author_repo = author_repo
        self.loan_repo = loan_repo

    def create_book(self, book_data: BookCreate):
        """
        Create a new book.
        """
        author = self.author_repo.get_author_by_id(book_data.author_id)
        if author is None:
            raise NotFoundException("Author does not exist")

        new_book = BookModel(
            title=book_data.title,
            isbn=book_data.isbn,
            published_date=book_data.published_date,
            author_id=book_data.author_id,
        )
        created = self.book_repo.create_book(new_book)

        schema_data = self._build_book_response(created)
        event = BookCreated(
            aggregate_id=created.id,
            data=schema_data.model_dump(mode="json"),
        )
        publish_domain_event(event)

        return schema_data

    def get_book_by_id(self, book_id: str):
        """
        Retrieve a book by its ID.
        """
        book = self.book_repo.get_book_by_id(book_id)
        if book is None:
            raise NotFoundException("Book not found")

        return self._build_book_response(book)

    def get_books(self):
        """
        Retrieve all books.
        """
        all_books = self.book_repo.get_books()
        result = []
        for book in all_books:
            result.append(self._build_book_response(book))
        return result

    def update_book(self, book_id: str, book_data: BookUpdate):
        """
        Update an existing book.
        """
        book = self.book_repo.get_book_by_id(book_id)
        if not book:
            raise NotFoundException("Book not found")

        if book_data.title:
            book.title = book_data.title
        if book_data.isbn:
            book.isbn = book_data.isbn
        if book_data.published_date:
            book.published_date = book_data.published_date
        if book_data.author_id:
            exists = self.author_repo.get_author_by_id(book_data.author_id)
            if not exists:
                raise NotFoundException("Author does not exist")
            book.author_id = book_data.author_id

        updated = self.book_repo.update_book(book)
        schema_data = self._build_book_response(updated)
        event = BookUpdated(
            aggregate_id=updated.id,
            data=schema_data.model_dump(mode="json"),
        )

        publish_domain_event(event)

        return schema_data

    def delete_book(self, book_id: str):
        """
        Delete a book by its ID.
        """
        book = self.book_repo.get_book_by_id(book_id)
        if book is None:
            raise NotFoundException("Book not found")

        has_active_loan = self.loan_repo.book_has_active_loan(book_id)
        if has_active_loan:
            raise ActiveLoanExistsException("Cannot delete book with active loans")

        event = BookDeleted(
            aggregate_id=book.id,
            data=self._build_book_response(book).model_dump(mode="json"),
        )

        self.book_repo.delete_book(book_id)

        publish_domain_event(event)

    def _build_book_response(self, book: BookModel) -> BookSchema:
        """
        Build a BookSchema response from a BookModel instance.
        """
        author = self.author_repo.get_author_by_id(book.author_id)
        author_name = author.name if author else None

        res = {
            "id": book.id,
            "title": book.title,
            "isbn": book.isbn,
            "published_date": book.published_date,
            "author_id": book.author_id,
            "author_name": author_name,
        }

        return BookSchema.model_validate(res)
