from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.author import Author
from app.repositories.author_repository import AuthorRepositoryInterface


class SQLAuthorRepository(AuthorRepositoryInterface):
    def __init__(self, sess: Session):
        self.session = sess

    def get_authors(self) -> List[Author]:
        """
        Retrieve all authors.

         Returns:
            List[Author]: A list of all Author objects.
        """
        return self.session.query(Author).all()

    def get_author_by_id(self, aid: str) -> Optional[Author]:
        """
        Retrieve an author by their ID.

        Args:
            aid (str): The ID of the author.

        Returns:
            Optional[Author]: The Author object if found, otherwise None.
        """
        return self.session.query(Author).filter(Author.id == aid).first()

    def create_author(self, new_author: Author) -> Author:
        """
        Create a new author in the repository.
        Args:
            new_author (Author): The Author object to create.
        Returns:
            Author: The newly created Author object with updated fields (e.g., ID).
        """
        self.session.add(new_author)
        self.session.flush()
        self.session.refresh(new_author)
        return new_author

    def update_author(self, author_data: Author) -> Author:
        """
        Update an existing author in the repository.

        Args:
            author_data (Author): The Author object to update.

        Returns:
            Author: The newly created Author object with updated fields (e.g., ID).

        """
        self.session.flush()
        self.session.refresh(author_data)
        return author_data

    def delete_author(self, author_id: str) -> None:
        """
        Delete an author by their ID.
        Args:
            author_id (str): The ID of the author to delete.
        """
        rec = self.get_author_by_id(author_id)
        if rec:
            self.session.delete(rec)
            self.session.flush()
