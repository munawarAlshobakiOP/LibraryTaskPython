from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.borrower import Borrower
from app.repositories.borrower_repository import BorrowerRepositoryInterface


class SQLBorrowerRepository(BorrowerRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def get_borrowers(self) -> List[Borrower]:
        return self.session.query(Borrower).all()

    def get_borrower_by_id(self, bid: str) -> Optional[Borrower]:
        return self.session.query(Borrower).filter(Borrower.id == bid).first()

    def create_borrower(self, b: Borrower) -> Borrower:
        self.session.add(b)
        self.session.flush()
        self.session.refresh(b)
        return b

    def update_borrower(self, borrower: Borrower) -> Borrower:
        self.session.flush()
        self.session.refresh(borrower)
        return borrower

    def delete_borrower(self, borrower_id: str) -> None:
        target = self.get_borrower_by_id(borrower_id)
        if target:
            self.session.delete(target)
            self.session.flush()

    def get_borrower_by_email(self, email_addr: str) -> Optional[Borrower]:
        return self.session.query(Borrower).filter(Borrower.email == email_addr).first()
