from datetime import datetime
from uuid import uuid4
from sqlalchemy import UUID, Column, DateTime, ForeignKey
from app.core.db import Base


class Loan(Base):
    __tablename__ = "Loans"
    book_id = Column(UUID(as_uuid=True), ForeignKey("Books.id", ondelete="CASCADE"))
    borrower_id = Column(
        UUID(as_uuid=True), ForeignKey("Borrowers.id", ondelete="CASCADE")
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    loan_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
