from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.book import Book


class BookRepositoryInterface(ABC):

    @abstractmethod
    def get_books(self) -> List[Book]:
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        pass

    @abstractmethod
    def create_book(self, book: Book) -> Book:
        pass

    @abstractmethod
    def update_book(self, book: Book) -> Book:
        pass

    @abstractmethod
    def delete_book(self, book_id: str) -> None:
        pass

    @abstractmethod
    def get_books_by_author_id(self, author_id: str) -> List[Book]:
        pass
