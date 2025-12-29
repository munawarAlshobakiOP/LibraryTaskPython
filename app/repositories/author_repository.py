from abc import ABC, abstractmethod
from typing import List

from app.models.author import Author


class AuthorRepositoryInterface(ABC):
    """
    Abstract base class for author repository. It
    defines the interface for author-related database operations.
    """

    @abstractmethod
    def get_authors(self) -> List["Author"]:
        """
        Retrieve all authors.

        """
        pass

    @abstractmethod
    def get_author_by_id(self, author_id: str) -> "Author":
        """
        Retrieve an author by their ID.
        """
        pass

    @abstractmethod
    def create_author(self, author: "Author") -> "Author":
        """
        Create a new author in the repository.
        """
        pass

    @abstractmethod
    def update_author(self, author: "Author") -> "Author":
        """
        Update an existing author in the repository.
        """
        pass

    @abstractmethod
    def delete_author(self, author_id: str) -> None:
        """
        Delete an author by their ID.
        """
        pass
        pass
