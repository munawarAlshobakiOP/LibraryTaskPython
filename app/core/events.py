from app.schemas.internal_event import InternalEvent
from app.schemas.domain_event import DomainEventSchema


def publish_internal_event(event: InternalEvent):
    print(event.model_dump_json(indent=2))


def publish_domain_event(event: DomainEventSchema):
    print(event.model_dump_json(indent=2))
