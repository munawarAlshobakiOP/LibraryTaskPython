from abc import ABC, abstractmethod
from typing import List
from app.models.author import Author


class AuthorRepositoryInterface(ABC):
    @abstractmethod
    def get_authors(self) -> List["Author"]:
        pass

    @abstractmethod
    def get_author_by_id(self, author_id: str) -> "Author":
        pass

    @abstractmethod
    def create_author(self, author: "Author") -> "Author":
        pass

    @abstractmethod
    def update_author(self, author: "Author") -> "Author":
        pass

    @abstractmethod
    def delete_author(self, author_id: str) -> None:

        pass
