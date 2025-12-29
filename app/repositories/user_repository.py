from abc import ABC, abstractmethod
from typing import Optional

from app.models.user import User


class UserRepositoryInterface(ABC):
    """
    Abstract base class for user repository. It
    defines the interface for user-related database operations.
    """

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.
        """
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        """
        Create a new user in the repository.
        """
        pass
