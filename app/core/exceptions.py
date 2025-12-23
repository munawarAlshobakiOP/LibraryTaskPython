class LibraryError(Exception):
    pass


class NotFoundException(LibraryError):
    def __init__(self, msg: str = "Resource not found"):
        self.msg = msg
        super().__init__(self.msg)


class BookAlreadyBorrowedException(LibraryError):
    def __init__(self, msg: str = "This book is already borrowed"):
        self.msg = msg
        super().__init__(self.msg)


class ActiveLoanExistsException(LibraryError):
    def __init__(self, msg: str = "Active loan exists for this resource"):
        self.msg = msg
        super().__init__(self.msg)


class BorrowerNotFoundException(LibraryError):
    def __init__(self, msg: str = "Borrower not found"):
        self.msg = msg
        super().__init__(self.msg)


class EmailAlreadyExistsException(LibraryError):
    def __init__(self, msg: str = "Email already exists"):
        self.msg = msg
        super().__init__(self.msg)
