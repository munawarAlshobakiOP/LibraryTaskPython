from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.book import Book
from app.models.loan import Loan
from app.repositories.book_repository import BookRepositoryInterface


class SQLBookRepository(BookRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def get_books(self) -> List[Book]:
        return self.session.query(Book).all()

    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        res = self.session.query(Book).filter(Book.Id == book_id).first()
        return res

    def create_book(self, book: Book) -> Book:
        self.session.add(book)
        self.session.flush()
        self.session.refresh(book)
        return book

    def update_book(self, book: Book) -> Book:
        self.session.flush()
        self.session.refresh(book)
        return book

    def delete_book(self, book_id: str) -> None:
        target = self.get_book_by_id(book_id)
        if target:
            self.session.delete(target)
            self.session.flush()

    def has_active_loan(self, book_id: str) -> bool:
        check = (
            self.session.query(Loan)
            .filter(Loan.BookId == book_id, Loan.ReturnDate.is_(None))
            .first()
        )
        return check is not None

    def get_books_by_author_id(self, author_id: str) -> List[Book]:
        return self.session.query(Book).filter(Book.AuthorId == author_id).all()
