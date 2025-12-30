from datetime import datetime
from uuid import uuid4
from typing import Optional

from app.core.exceptions import ActiveLoanExistsException, NotFoundException
from app.models.borrower import Borrower as BorrowerModel
from app.repositories.borrower_repository import BorrowerRepositoryInterface
from app.repositories.loan_repository import LoanRepositoryInterface
from app.schemas.borrower import (
    BorrowerCreate,
    BorrowerUpdate,
    Borrower as BorrowerSchema,
)
from app.schemas.domain_event import BorrowerCreated, BorrowerUpdated, BorrowerDeleted
from app.schemas.loan import Loan as LoanSchema
from app.core.events import publish_domain_event


class BorrowerService:
    def __init__(
        self,
        borrower_repo: BorrowerRepositoryInterface,
        loan_repo: LoanRepositoryInterface,
    ):
        """
        Initialize the BorrowerService with the given repositories.
        """
        self.borrower_repo = borrower_repo
        self.loan_repo = loan_repo

    def get_borrowers(self):
        """
        Retrieve all borrowers.
        """
        records = self.borrower_repo.get_borrowers()
        blist = []
        for r in records:
            blist.append(BorrowerSchema.model_validate(r))
        return blist

    def get_borrower_by_id(self, bid: str):
        borrower = self.borrower_repo.get_borrower_by_id(bid)
        if not borrower:
            raise NotFoundException("Borrower not found")
        return BorrowerSchema.model_validate(borrower)

    def create_borrower(self, data: BorrowerCreate) -> BorrowerSchema:
        obj = BorrowerModel(
            name=data.name,
            email=data.email,
            phone=data.phone,
        )
        res = self.borrower_repo.create_borrower(obj)

        schema_data = BorrowerSchema.model_validate(res)
        event = BorrowerCreated(
            aggregate_id=res.id,
            data=schema_data.model_dump(mode="json"),
        )

        publish_domain_event(event)

        return schema_data

    def update_borrower(self, bid: str, data: BorrowerUpdate) -> BorrowerSchema:
        borrower = self.borrower_repo.get_borrower_by_id(bid)
        if borrower is None:
            raise NotFoundException("Borrower not found")

        if data.name is not None:
            borrower.name = data.name
        if data.email is not None:
            borrower.email = data.email
        if data.phone is not None:
            borrower.phone = data.phone
        updated = self.borrower_repo.update_borrower(borrower)

        schema_data = BorrowerSchema.model_validate(updated)
        event = BorrowerUpdated(
            aggregate_id=updated.id,
            data=schema_data.model_dump(mode="json"),
        )

        publish_domain_event(event)

        return schema_data

    def delete_borrower(self, bid: str):
        borrower = self.borrower_repo.get_borrower_by_id(bid)
        if not borrower:
            raise NotFoundException("Borrower not found")

        active_loans = self.loan_repo.get_active_loans_by_borrower(bid)
        if len(active_loans) > 0:
            raise ActiveLoanExistsException("Cannot delete borrower with active loans")

        event = BorrowerDeleted(
            aggregate_id=borrower.id,
            data=BorrowerSchema.model_validate(borrower).model_dump(mode="json"),
        )

        self.borrower_repo.delete_borrower(bid)

        publish_domain_event(event)

        return True

    def get_borrower_profile_with_loans(self, bid: str):
        borrower_data = self.get_borrower_by_id(bid)
        loans = self.loan_repo.get_loans_by_borrower_id(bid)

        loan_list = []
        for loan in loans:
            loan_list.append(LoanSchema.model_validate(loan))

        return {"borrower": borrower_data, "loans": loan_list}
