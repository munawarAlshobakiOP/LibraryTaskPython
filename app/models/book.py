from uuid import uuid4
from sqlalchemy import UUID, Column, String, DateTime, ForeignKey
from datetime import datetime
from app.core.db import Base


class Book(Base):
    __tablename__ = "Books"
    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    Title = Column(String)
    ISBN = Column(String)
    PublishedDate = Column(String)
    AuthorId = Column(UUID(as_uuid=True), ForeignKey("Authors.Id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
