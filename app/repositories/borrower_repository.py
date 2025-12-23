from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.borrower import Borrower


class BorrowerRepositoryInterface(ABC):
    @abstractmethod
    def get_borrowers(self) -> List[Borrower]:
        pass

    @abstractmethod
    def get_borrower_by_id(self, borrower_id: str) -> Optional[Borrower]:
        pass

    @abstractmethod
    def create_borrower(self, borrower: Borrower) -> Borrower:
        pass

    @abstractmethod
    def update_borrower(self, borrower: Borrower) -> Borrower:
        pass

    @abstractmethod
    def delete_borrower(self, borrower_id: str) -> None:
        pass
