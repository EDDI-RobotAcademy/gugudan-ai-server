from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database.session import Base


class InquiryModel(Base):
    __tablename__ = "inquiry"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(30), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(30), default="PENDING", nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    replies = relationship(
        "InquiryReplyModel",
        backref="inquiry",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index('idx_inquiry_account_created', 'account_id', 'created_at'),
        Index('idx_inquiry_status_created', 'status', 'created_at'),
    )

    def __repr__(self) -> str:
        return f"<InquiryModel(id={self.id}, account_id={self.account_id}, status={self.status})>"