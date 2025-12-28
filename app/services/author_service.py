from app.repositories.author_repository import AuthorRepositoryInterface
from app.repositories.book_repository import BookRepositoryInterface
from app.schemas.author import AuthorCreate, AuthorUpdate, Author as AuthorSchema
from app.schemas.book import Book as BookSchema
from app.models.author import Author as AuthorModel
from app.core.exceptions import NotFoundException


class AuthorService:
    def __init__(
        self, author_repo: AuthorRepositoryInterface, book_repo: BookRepositoryInterface
    ):
        self.author_repo = author_repo
        self.book_repo = book_repo

    def create_author(self, data: AuthorCreate):
        obj = AuthorModel(name=data.name, bio=data.bio)
        res = self.author_repo.create_author(obj)
        return AuthorSchema.model_validate(res)

    def get_author_by_id(self, auth_id: str):
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
        records = self.author_repo.get_authors()

        if not records:
            raise NotFoundException("No authors found")

        result = []
        for r in records:
            result.append(AuthorSchema.model_validate(r))
        return result

    def update_author(self, aid: str, data: AuthorUpdate):
        author = self.author_repo.get_author_by_id(aid)

        if author is None:
            raise NotFoundException("Author not found")

        if data.name is not None:
            author.name = data.name

        if data.bio is not None:
            author.bio = data.bio

        updated = self.author_repo.update_author(author)
        return AuthorSchema.model_validate(updated)

    def delete_author(self, aid: str):
        author = self.author_repo.get_author_by_id(aid)
        if not author:
            raise NotFoundException("Author not found")

        self.author_repo.delete_author(aid)
