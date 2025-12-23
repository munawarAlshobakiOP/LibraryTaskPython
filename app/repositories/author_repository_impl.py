from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.author import Author
from app.repositories.author_repository import AuthorRepositoryInterface


class SQLAuthorRepository(AuthorRepositoryInterface):
    def __init__(self, sess: Session):
        self.session = sess

    def get_authors(self) -> List[Author]:
        return self.session.query(Author).all()

    def get_author_by_id(self, aid: str) -> Optional[Author]:
        return self.session.query(Author).filter(Author.Id == aid).first()

    def create_author(self, new_author: Author) -> Author:
        self.session.add(new_author)
        self.session.flush()
        self.session.refresh(new_author)
        return new_author

    def update_author(self, author_data: Author) -> Author:
        self.session.flush()
        self.session.refresh(author_data)
        return author_data

    def delete_author(self, author_id: str) -> None:
        rec = self.get_author_by_id(author_id)
        if rec:
            self.session.delete(rec)
            self.session.flush()
