from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.loan import Loan
from app.repositories.book_repository import BookRepositoryInterface


class SQLBookRepository(BookRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def get_books(self) -> List[Book]:
        """
        Retrieve all books.
        Returns:
            List[Book]: A list of all Book objects.
        """
        return self.session.query(Book).all()

    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """
        Retrieve a book by its ID.
        Args:
            book_id (str): The ID of the book.
        Returns:
            Optional[Book]: The Book object if found, otherwise None.
        """
        res = self.session.query(Book).filter(Book.id == book_id).first()
        return res

    def create_book(self, book: Book) -> Book:
        """
        Create a new book in the repository.
        Args:
            book (Book): The Book object to create.
        Returns:
            Book: The newly created Book object with updated fields (e.g., ID).
        """
        self.session.add(book)
        self.session.flush()
        self.session.refresh(book)
        return book

    def update_book(self, book: Book) -> Book:
        """
        Update an existing book in the repository.
        Args:
            book (Book): The Book object to update.
        Returns:
            Book: The updated Book object.
        """
        self.session.flush()
        self.session.refresh(book)
        return book

    def delete_book(self, book_id: str) -> None:
        """
        Delete a book by its ID.
        Args:
            book_id (str): The ID of the book to delete.

        """
        target = self.get_book_by_id(book_id)
        if target:
            self.session.delete(target)
            self.session.flush()

    def has_active_loan(self, book_id: str) -> bool:
        """
        Check if a book has an active loan.
        Args:
            book_id (str): The ID of the book to check.
        Returns:
            bool: True if the book has an active loan, False otherwise.
        """
        check = (
            self.session.query(Loan)
            .filter(Loan.book_id == book_id, Loan.return_date.is_(None))
            .first()
        )
        return check is not None

    def get_books_by_author_id(self, author_id: str) -> List[Book]:
        """
        Retrieve all books by a specific author.
        Args:
            author_id (str): The ID of the author.
        Returns:
            List[Book]: A list of Book objects by the specified author.
        """
        return self.session.query(Book).filter(Book.author_id == author_id).all()
