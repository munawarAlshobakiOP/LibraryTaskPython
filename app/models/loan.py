from uuid import uuid4
from sqlalchemy import UUID, Column, DateTime, String, ForeignKey
from datetime import datetime
from app.core.db import Base


class Loan(Base):
    __tablename__ = "Loans"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("Books.id", ondelete="CASCADE"))
    borrower_id = Column(
        UUID(as_uuid=True), ForeignKey("Borrowers.id", ondelete="CASCADE")
    )
    loan_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
