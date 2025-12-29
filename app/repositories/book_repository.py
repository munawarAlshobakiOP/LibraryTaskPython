from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.book import Book


class BookRepositoryInterface(ABC):
    """
    Abstract base class for book repository. It
    defines the interface for book-related database operations.
    """

    @abstractmethod
    def get_books(self) -> List[Book]:
        """
        Retrieve all books.
        """
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """
        Retrieve a book by its ID.
        """
        pass

    @abstractmethod
    def create_book(self, book: Book) -> Book:
        """
        Create a new book in the repository.
        """
        pass

    @abstractmethod
    def update_book(self, book: Book) -> Book:
        """
        Update an existing book in the repository.
        """
        pass

    @abstractmethod
    def delete_book(self, book_id: str) -> None:
        """
        Delete a book by its ID.
        """
        pass

    @abstractmethod
    def get_books_by_author_id(self, author_id: str) -> List[Book]:
        """
        Retrieve all books by a specific author.
        """
        pass
