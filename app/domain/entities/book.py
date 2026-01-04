from app.domain.constant.event_types import EventTypes
from app.domain.entities.domain_event import DomainEventSchema


class BookCreated(DomainEventSchema):
    event_type: str = EventTypes.BOOK_CREATED
    aggregate_type: str = "book"


class BookUpdated(DomainEventSchema):
    event_type: str = EventTypes.BOOK_UPDATED
    aggregate_type: str = "book"


class BookDeleted(DomainEventSchema):
    event_type: str = EventTypes.BOOK_DELETED
    aggregate_type: str = "book"
