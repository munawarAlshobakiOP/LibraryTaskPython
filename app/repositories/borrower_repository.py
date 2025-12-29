from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.borrower import Borrower


class BorrowerRepositoryInterface(ABC):
    """
    Abstract base class for borrower repository. It
    defines the interface for borrower-related database operations.
    """

    @abstractmethod
    def get_borrowers(self) -> List[Borrower]:
        """
        Retrieve all borrowers.
        """
        pass

    @abstractmethod
    def get_borrower_by_id(self, borrower_id: str) -> Optional[Borrower]:
        """
        Retrieve a borrower by their ID.
        """
        pass

    @abstractmethod
    def create_borrower(self, borrower: Borrower) -> Borrower:
        """
        Create a new borrower in the repository.
        """
        pass

    @abstractmethod
    def update_borrower(self, borrower: Borrower) -> Borrower:
        """
        Update an existing borrower in the repository.
        """
        pass

    @abstractmethod
    def delete_borrower(self, borrower_id: str) -> None:
        """
        Delete a borrower by their ID.
        """
        pass
