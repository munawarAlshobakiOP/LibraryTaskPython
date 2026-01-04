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
