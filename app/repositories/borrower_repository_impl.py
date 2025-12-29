from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.borrower import Borrower
from app.repositories.borrower_repository import BorrowerRepositoryInterface


class SQLBorrowerRepository(BorrowerRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def get_borrowers(self) -> List[Borrower]:
        """
        Retrieve all borrowers.
        Returns:
            List[Borrower]: A list of all Borrower objects.
        """
        return self.session.query(Borrower).all()

    def get_borrower_by_id(self, bid: str) -> Optional[Borrower]:
        """
        Retrieve a borrower by their ID.
        Args:
            bid (str): The ID of the borrower.
        Returns:
            Optional[Borrower]: The Borrower object if found, otherwise None.
        """
        return self.session.query(Borrower).filter(Borrower.id == bid).first()

    def create_borrower(self, b: Borrower) -> Borrower:
        """
        Create a new borrower in the repository.
        Args:
            b (Borrower): The Borrower object to create.
        Returns:
            Borrower: The newly created Borrower object with updated fields (e.g., ID).
        """
        self.session.add(b)
        self.session.flush()
        self.session.refresh(b)
        return b

    def update_borrower(self, borrower: Borrower) -> Borrower:
        """
        Update an existing borrower in the repository.
        Args:
            borrower (Borrower): The Borrower object to update.
        Returns:
            Borrower: The updated Borrower object.
        """
        self.session.flush()
        self.session.refresh(borrower)
        return borrower

    def delete_borrower(self, borrower_id: str) -> None:
        """
        Delete a borrower by their ID.
        Args:
            borrower_id (str): The ID of the borrower to delete.

        """
        target = self.get_borrower_by_id(borrower_id)
        if target:
            self.session.delete(target)
            self.session.flush()

    def get_borrower_by_email(self, email_addr: str) -> Optional[Borrower]:
        """
        Retrieve a borrower by their email address.
        Args:
            email_addr (str): The email address of the borrower.
        Returns:
            Optional[Borrower]: The Borrower object if found, otherwise None.
        """
        return self.session.query(Borrower).filter(Borrower.email == email_addr).first()
