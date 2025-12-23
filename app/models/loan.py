from uuid import uuid4
from sqlalchemy import UUID, Column, DateTime, String, ForeignKey
from datetime import datetime
from app.core.db import Base


class Loan(Base):
    __tablename__ = "Loans"
    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    BookId = Column(UUID(as_uuid=True), ForeignKey("Books.Id", ondelete="CASCADE"))
    BorrowerId = Column(
        UUID(as_uuid=True), ForeignKey("Borrowers.Id", ondelete="CASCADE")
    )
    LoanDate = Column(DateTime, default=datetime.utcnow)
    ReturnDate = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
