import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    password_hash = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
