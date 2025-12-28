from uuid import uuid4
from sqlalchemy import UUID, Column, String, DateTime, ForeignKey
from datetime import datetime
from app.core.db import Base


class Book(Base):
    __tablename__ = "Books"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String)
    isbn = Column(String)
    published_date = Column(DateTime)
    author_id = Column(UUID(as_uuid=True), ForeignKey("Authors.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
