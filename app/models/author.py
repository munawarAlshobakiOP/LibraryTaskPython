from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, String, DateTime

from app.core.db import Base


class Author(Base):
    __tablename__ = "Authors"

    bio = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
