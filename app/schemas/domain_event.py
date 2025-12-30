from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from datetime import datetime
from typing import Any, Dict


class DomainEventSchema(BaseModel):
    """
    Base class for all domain events.
    """

    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    aggregate_type: str
    aggregate_id: UUID
    data: Dict[str, Any]


class AuthorCreated(DomainEventSchema):
    event_type: str = "author.created"
    aggregate_type: str = "author"


class AuthorUpdated(DomainEventSchema):
    event_type: str = "author.updated"
    aggregate_type: str = "author"


class AuthorDeleted(DomainEventSchema):
    event_type: str = "author.deleted"
    aggregate_type: str = "author"


class BookCreated(DomainEventSchema):
    event_type: str = "book.created"
    aggregate_type: str = "book"


class BookUpdated(DomainEventSchema):
    event_type: str = "book.updated"
    aggregate_type: str = "book"


class BookDeleted(DomainEventSchema):
    event_type: str = "book.deleted"
    aggregate_type: str = "book"


class BorrowerCreated(DomainEventSchema):
    event_type: str = "borrower.created"
    aggregate_type: str = "borrower"


class BorrowerUpdated(DomainEventSchema):
    event_type: str = "borrower.updated"
    aggregate_type: str = "borrower"


class BorrowerDeleted(DomainEventSchema):
    event_type: str = "borrower.deleted"
    aggregate_type: str = "borrower"


class LoanCreated(DomainEventSchema):
    event_type: str = "loan.created"
    aggregate_type: str = "loan"


class LoanReturned(DomainEventSchema):
    event_type: str = "loan.returned"
    aggregate_type: str = "loan"
