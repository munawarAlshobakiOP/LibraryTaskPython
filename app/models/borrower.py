from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, String

from app.core.db import Base


class Borrower(Base):
    __tablename__ = "Borrowers"

    created_at = Column(DateTime, default=datetime.utcnow)
    email = Column(String, unique=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    phone = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
