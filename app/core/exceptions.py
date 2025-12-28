class LibraryError(Exception):
    """Base class for all library-related exceptions."""

    pass


class NotFoundException(LibraryError):
    """Exception raised when a requested resource is not found."""

    def __init__(self, msg: str = "Resource not found"):
        self.msg = msg
        super().__init__(self.msg)


class BookAlreadyBorrowedException(LibraryError):
    """Exception raised when a book is already borrowed."""

    def __init__(self, msg: str = "This book is already borrowed"):
        self.msg = msg
        super().__init__(self.msg)


class ActiveLoanExistsException(LibraryError):
    """Exception raised when an active loan exists for a resource."""

    def __init__(self, msg: str = "Active loan exists for this resource"):
        self.msg = msg
        super().__init__(self.msg)


class BorrowerNotFoundException(LibraryError):
    """Exception raised when a borrower is not found."""

    def __init__(self, msg: str = "Borrower not found"):
        self.msg = msg
        super().__init__(self.msg)


class EmailAlreadyExistsException(LibraryError):
    """Exception raised when an email already exists."""

    def __init__(self, msg: str = "Email already exists"):
        self.msg = msg
        super().__init__(self.msg)
