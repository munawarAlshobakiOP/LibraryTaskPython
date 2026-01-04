"""Event topics and constants."""

from typing import Final


class EventTypes:
    """Event type constants"""

    # Subscription Events
    AUTHOR_CREATED: Final[str] = "author.created"
    AUTHOR_UPDATED: Final[str] = "author.updated"
    AUTHOR_DELETED: Final[str] = "author.deleted"

    BOOK_CREATED: Final[str] = "book.created"
    BOOK_UPDATED: Final[str] = "book.updated"
    BOOK_DELETED: Final[str] = "book.deleted"

    BORROWER_CREATED: Final[str] = "borrower.created"
    BORROWER_UPDATED: Final[str] = "borrower.updated"
    BORROWER_DELETED: Final[str] = "borrower.deleted"

    LOAN_CREATED: Final[str] = "loan.created"
    LOAN_RETURNED: Final[str] = "loan.returned"

