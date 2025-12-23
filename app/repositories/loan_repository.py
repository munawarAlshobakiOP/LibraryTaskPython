from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.loan import Loan


class LoanRepositoryInterface(ABC):

    @abstractmethod
    def get_active_loans(self) -> List[Loan]:
        pass

    @abstractmethod
    def return_loan(self, loan_id: str) -> Loan:
        pass

    @abstractmethod
    def get_active_loans_by_borrower(self, borrower_id: str) -> List[Loan]:
        pass

    @abstractmethod
    def get_loans(self) -> List[Loan]:
        pass

    @abstractmethod
    def get_loan_by_id(self, loan_id: str) -> Optional[Loan]:
        pass

    @abstractmethod
    def create_loan(self, loan: Loan) -> Loan:
        pass

    @abstractmethod
    def update_loan(self, loan: Loan) -> Loan:
        pass

    @abstractmethod
    def book_has_active_loan(self, book_id: str) -> bool:
        pass

    @abstractmethod
    def get_loans_by_borrower_id(self, borrower_id: str) -> List[Loan]:
        pass
