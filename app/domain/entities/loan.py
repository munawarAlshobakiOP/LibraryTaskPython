from app.domain.constant.event_types import EventTypes
from app.domain.entities.domain_event import DomainEventSchema


class LoanCreated(DomainEventSchema):
    event_type: str = EventTypes.LOAN_CREATED
    aggregate_type: str = "loan"


class LoanReturned(DomainEventSchema):
    event_type: str = EventTypes.LOAN_RETURNED
    aggregate_type: str = "loan"
