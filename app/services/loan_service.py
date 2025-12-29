from datetime import datetime

from app.core.exceptions import BookAlreadyBorrowedException, NotFoundException
from app.models.loan import Loan as LoanModel
from app.repositories.loan_repository import LoanRepositoryInterface
from app.schemas.loan import LoanCreate, Loan as LoanSchema


class LoanService:
    def __init__(self, repo: LoanRepositoryInterface):
        """
        Initialize the LoanService with the given repository.
        """
        self.repo = repo

    def get_active_loans(self):
        """
        Retrieve all active loans.
        returns:
            List[LoanSchema]: A list of active LoanSchema objects.
        """
        active = self.repo.get_active_loans()
        return [LoanSchema.model_validate(active_loan) for active_loan in active]

    def get_borrower_loan_history(self, borrower_id: str):
        """
        Retrieve the loan history for a specific borrower.
        Args:
            borrower_id (str): The ID of the borrower.
        Returns:
            List[LoanSchema]: A list of LoanSchema objects for the borrower.
        """
        loans = self.repo.get_loans_by_borrower_id(borrower_id)
        result = []
        for loan in loans:
            result.append(LoanSchema.model_validate(loan))
        return result

    def create_loan(self, data: LoanCreate):
        """
        Create a new loan.
        Args:
            data (LoanCreate): The data for creating a new loan.
        Returns:
            LoanSchema: The created LoanSchema object.
        """
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
        """
        Return a loan by its ID.
        Args:
            loan_id (str): The ID of the loan to return.
        Returns:
            LoanSchema: The updated LoanSchema object with the return date set.
        """
        loan = self.repo.get_loan_by_id(loan_id)

        if loan is None:
            raise NotFoundException("Loan not found")

        if loan.return_date is not None:
            return LoanSchema.model_validate(loan)

        returned = self.repo.return_loan(loan_id)
        return LoanSchema.model_validate(returned)

    def _parse_dt(self, s):
        """
        Parse a date string into a datetime object.
        Args:
            s (str): The date string to parse.
        Returns:
            Optional[datetime]: The parsed datetime object, or None if parsing fails.
        """
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
