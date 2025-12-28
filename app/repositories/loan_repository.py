from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.loan import Loan


class LoanRepositoryInterface(ABC):
    """
    Abstract base class for loan repository. It
    defines the interface for loan-related database operations.
    """

    @abstractmethod
    def get_active_loans(self) -> List[Loan]:
        """
        Retrieve all active loans.
        """
        pass

    @abstractmethod
    def return_loan(self, loan_id: str) -> Loan:
        """
        set return a loan by its ID.
        """
        pass

    @abstractmethod
    def get_active_loans_by_borrower(self, borrower_id: str) -> List[Loan]:
        """
        Retrieve all active loans for a specific borrower.
        """
        pass

    @abstractmethod
    def get_loans(self) -> List[Loan]:
        """
        Retrieve all loans.
        """
        pass

    @abstractmethod
    def get_loan_by_id(self, loan_id: str) -> Optional[Loan]:
        """
        Retrieve a loan by its ID.
        """
        pass

    @abstractmethod
    def create_loan(self, loan: Loan) -> Loan:
        """
        Create a new loan in the repository.
        """
        pass

    @abstractmethod
    def update_loan(self, loan: Loan) -> Loan:
        """
        Update an existing loan in the repository.
        """
        pass

    @abstractmethod
    def book_has_active_loan(self, book_id: str) -> bool:
        """
        Check if a book has an active loan.
        """
        pass

    @abstractmethod
    def get_loans_by_borrower_id(self, borrower_id: str) -> List[Loan]:
        """
        Retrieve all loans for a specific borrower.
        """
        pass
