from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.loan import Loan
from app.repositories.loan_repository import LoanRepositoryInterface


class SQLLoanRepository(LoanRepositoryInterface):
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_active_loans(self) -> List[Loan]:
        return self.session.query(Loan).filter(Loan.return_date.is_(None)).all()

    def get_loans_by_borrower_id(self, borrower_id: str) -> List[Loan]:
        res = self.session.query(Loan).filter(Loan.borrower_id == borrower_id).all()
        return res

    def get_active_loans_by_borrower(self, borrower_id: str) -> List[Loan]:
        return (
            self.session.query(Loan)
            .filter(Loan.borrower_id == borrower_id, Loan.return_date.is_(None))
            .all()
        )

    def get_loans(self) -> List[Loan]:
        return self.session.query(Loan).all()

    def get_loan_by_id(self, loan_id: str) -> Optional[Loan]:
        return self.session.query(Loan).filter(Loan.id == loan_id).first()

    def create_loan(self, loan_obj: Loan) -> Loan:
        self.session.add(loan_obj)
        self.session.flush()
        self.session.refresh(loan_obj)
        return loan_obj

    def update_loan(self, loan: Loan) -> Loan:
        self.session.flush()
        self.session.refresh(loan)
        return loan

    def return_loan(self, loan_id: str) -> Loan:
        target_loan = self.get_loan_by_id(loan_id)
        if target_loan:
            target_loan.return_date = datetime.utcnow()
            self.session.flush()
            self.session.refresh(target_loan)
        return target_loan

    def book_has_active_loan(self, book_id: str) -> bool:
        active = (
            self.session.query(Loan)
            .filter(Loan.book_id == book_id, Loan.return_date.is_(None))
            .first()
        )
        return active is not None
