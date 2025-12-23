from app.repositories.book_repository import BookRepositoryInterface
from app.repositories.author_repository import AuthorRepositoryInterface
from app.repositories.loan_repository import LoanRepositoryInterface
from app.schemas.book import BookCreate, BookUpdate, Book as BookSchema
from app.models.book import Book as BookModel
from app.core.exceptions import NotFoundException, ActiveLoanExistsException


class BookService:
    def __init__(
        self,
        book_repo: BookRepositoryInterface,
        author_repo: AuthorRepositoryInterface,
        loan_repo: LoanRepositoryInterface,
    ):
        self.book_repo = book_repo
        self.author_repo = author_repo
        self.loan_repo = loan_repo

    def create_book(self, book_data: BookCreate):
        author = self.author_repo.get_author_by_id(book_data.author_id)
        if author is None:
            raise NotFoundException("Author does not exist")

        new_book = BookModel(
            Title=book_data.title,
            ISBN=book_data.isbn,
            PublishedDate=book_data.published_date,
            AuthorId=book_data.author_id,
        )

        created = self.book_repo.create_book(new_book)
        return self._build_book_response(created)

    def get_book_by_id(self, book_id: str):
        book = self.book_repo.get_book_by_id(book_id)
        if book is None:
            raise NotFoundException("Book not found")

        return self._build_book_response(book)

    def get_books(self):
        all_books = self.book_repo.get_books()
        result = []
        for book in all_books:
            result.append(self._build_book_response(book))
        return result

    def update_book(self, book_id: str, book_data: BookUpdate):
        book = self.book_repo.get_book_by_id(book_id)
        if not book:
            raise NotFoundException("Book not found")

        if book_data.title:
            book.Title = book_data.title
        if book_data.isbn:
            book.ISBN = book_data.isbn
        if book_data.published_date:
            book.PublishedDate = book_data.published_date

        if book_data.author_id:
            exists = self.author_repo.get_author_by_id(book_data.author_id)
            if not exists:
                raise NotFoundException("Author does not exist")
            book.AuthorId = book_data.author_id

        updated = self.book_repo.update_book(book)
        return self._build_book_response(updated)

    def delete_book(self, book_id: str):
        book = self.book_repo.get_book_by_id(book_id)
        if book is None:
            raise NotFoundException("Book not found")

        has_active_loan = self.loan_repo.book_has_active_loan(book_id)
        if has_active_loan:
            raise ActiveLoanExistsException("Cannot delete book with active loans")

        self.book_repo.delete_book(book_id)

    def _build_book_response(self, book: BookModel) -> BookSchema:
        author = self.author_repo.get_author_by_id(book.AuthorId)
        author_name = author.Name if author else None

        res = {
            "Id": book.Id,
            "Title": book.Title,
            "ISBN": book.ISBN,
            "PublishedDate": book.PublishedDate,
            "AuthorId": book.AuthorId,
            "AuthorName": author_name,
        }

        return BookSchema.model_validate(res)
