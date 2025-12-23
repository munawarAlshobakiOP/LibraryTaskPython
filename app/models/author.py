from uuid import uuid4
from sqlalchemy import UUID, Column, String, DateTime
from datetime import datetime
from app.core.db import Base


class Author(Base):
    __tablename__ = "Authors"
    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    Name = Column(String)
    Bio = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
