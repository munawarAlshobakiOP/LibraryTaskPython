from app.domain.constant.event_types import EventTypes
from app.domain.entities.domain_event import DomainEventSchema


class BorrowerCreated(DomainEventSchema):
    event_type: str = EventTypes.BORROWER_CREATED
    aggregate_type: str = "borrower"


class BorrowerUpdated(DomainEventSchema):
    event_type: str = EventTypes.BORROWER_UPDATED
    aggregate_type: str = "borrower"


class BorrowerDeleted(DomainEventSchema):
    event_type: str = EventTypes.BORROWER_DELETED
    aggregate_type: str = "borrower"
