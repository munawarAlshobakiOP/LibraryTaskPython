from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from datetime import datetime
from typing import Any, Dict, Optional


class InternalEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=datetime.utcnow)


class LoanValidationFailed(InternalEvent):
    event_type: str = "Loan.validation_failed"
    reason: str
    validation_errors: Dict[str, Any] = Field(default_factory=dict)


class SecurityAuthFailed(InternalEvent):
    event_type: str = "Security.auth_failed"
    reason: str
