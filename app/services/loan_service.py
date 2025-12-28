from app.repositories.loan_repository import LoanRepositoryInterface
from app.core.exceptions import BookAlreadyBorrowedException, NotFoundException
from app.models.loan import Loan as LoanModel
from app.schemas.loan import LoanCreate, Loan as LoanSchema
from datetime import datetime


class LoanService:
    def __init__(self, repo: LoanRepositoryInterface):
        self.repo = repo

    def get_active_loans(self):
        active = self.repo.get_active_loans()
        return [LoanSchema.model_validate(active_loan) for active_loan in active]

    def get_borrower_loan_history(self, borrower_id: str):
        loans = self.repo.get_loans_by_borrower_id(borrower_id)
        result = []
        for loan in loans:
            result.append(LoanSchema.model_validate(loan))
        return result

    def create_loan(self, data: LoanCreate):
        if self.repo.book_has_active_loan(data.book_id):
            raise BookAlreadyBorrowedException(
                "A book cannot be loaned if it currently has an active loan"
            )

        ldate = self._parse_dt(data.loan_date)
        if not ldate:
            ldate = datetime.utcnow()

        rdate = self._parse_dt(data.return_date) if data.return_date else None

        loan_item = LoanModel(
            book_id=data.book_id,
            borrower_id=data.borrower_id,
            loan_date=ldate,
            return_date=rdate,
        )

        created = self.repo.create_loan(loan_item)
        return LoanSchema.model_validate(created)

    def return_loan(self, loan_id: str):
        loan = self.repo.get_loan_by_id(loan_id)

        if loan is None:
            raise NotFoundException("Loan not found")

        if loan.return_date is not None:
            return LoanSchema.model_validate(loan)

        returned = self.repo.return_loan(loan_id)
        return LoanSchema.model_validate(returned)

    def _parse_dt(self, s):
        if not s:
            return None

        try:
            return datetime.fromisoformat(s)
        except ValueError:
            pass

        try:
            return datetime.strptime(s, "%d-%m-%Y")
        except ValueError:
            return None
