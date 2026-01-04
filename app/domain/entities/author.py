from app.domain.entities.domain_event import DomainEventSchema
from app.domain.constant.event_types import EventTypes


class AuthorCreated(DomainEventSchema):
    event_type: str = EventTypes.AUTHOR_CREATED
    aggregate_type: str = "author"


class AuthorUpdated(DomainEventSchema):
    event_type: str = EventTypes.AUTHOR_UPDATED
    aggregate_type: str = "author"


class AuthorDeleted(DomainEventSchema):
    event_type: str = EventTypes.AUTHOR_DELETED
    aggregate_type: str = "author"
