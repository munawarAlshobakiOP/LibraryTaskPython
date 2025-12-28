from uuid import uuid4
from sqlalchemy import UUID, Column, DateTime, String
from datetime import datetime
from app.core.db import Base


class Borrower(Base):
    __tablename__ = "Borrowers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
