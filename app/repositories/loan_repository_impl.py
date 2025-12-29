from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.loan import Loan
from app.repositories.loan_repository import LoanRepositoryInterface


class SQLLoanRepository(LoanRepositoryInterface):

    def __init__(self, db_session: Session):
        self.session = db_session

    def get_active_loans(self) -> List[Loan]:
        """
        Retrieve all active loans (loans that have not been returned).
        Returns:
            List[Loan]: A list of active Loan objects.
        """
        return self.session.query(Loan).filter(Loan.return_date.is_(None)).all()

    def get_loans_by_borrower_id(self, borrower_id: str) -> List[Loan]:
        """
        Retrieve all loans for a specific borrower.
        Args:
            borrower_id (str): The ID of the borrower.
        Returns:
            List[Loan]: A list of Loan objects for the specified borrower.
        """
        res = self.session.query(Loan).filter(Loan.borrower_id == borrower_id).all()
        return res

    def get_active_loans_by_borrower(self, borrower_id: str) -> List[Loan]:
        """
        Retrieve all active loans for a specific borrower.
        Args:
            borrower_id (str): The ID of the borrower.
        Returns:
            List[Loan]: A list of active Loan objects for the specified borrower.
        """
        return (
            self.session.query(Loan)
            .filter(Loan.borrower_id == borrower_id, Loan.return_date.is_(None))
            .all()
        )

    def get_loans(self) -> List[Loan]:
        """
        Retrieve all loans.
        Returns:
            List[Loan]: A list of all Loan objects.

        """
        return self.session.query(Loan).all()

    def get_loan_by_id(self, loan_id: str) -> Optional[Loan]:
        """
        Retrieve a loan by its ID.
        Args:
            loan_id (str): The ID of the loan.
        Returns:
            Optional[Loan]: The Loan object if found, otherwise None.
        """
        return self.session.query(Loan).filter(Loan.id == loan_id).first()

    def create_loan(self, loan_obj: Loan) -> Loan:
        """
        Create a new loan in the repository.
        Args:
            loan_obj (Loan): The Loan object to create.
        Returns:
            Loan: The newly created Loan object with updated fields (e.g., ID).
        """
        self.session.add(loan_obj)
        self.session.flush()
        self.session.refresh(loan_obj)
        return loan_obj

    def update_loan(self, loan: Loan) -> Loan:
        """
        Update an existing loan in the repository.
        Args:
            loan (Loan): The Loan object to update.
        Returns:
            Loan: The updated Loan object.
        """
        self.session.flush()
        self.session.refresh(loan)
        return loan

    def return_loan(self, loan_id: str) -> Loan:
        """
        set return a loan by its ID.
        Args:
            loan_id (str): The ID of the loan to return.
        Returns:
            Loan: The updated Loan object with the return date set.
        """
        target_loan = self.get_loan_by_id(loan_id)
        if target_loan:
            target_loan.return_date = datetime.utcnow()
            self.session.flush()
            self.session.refresh(target_loan)
        return target_loan

    def book_has_active_loan(self, book_id: str) -> bool:
        """
        Check if a book has an active loan.
        Args:
            book_id (str): The ID of the book to check.
        Returns:
            bool: True if the book has an active loan, False otherwise.
        """
        active = (
            self.session.query(Loan)
            .filter(Loan.book_id == book_id, Loan.return_date.is_(None))
            .first()
        )
        return active is not None
