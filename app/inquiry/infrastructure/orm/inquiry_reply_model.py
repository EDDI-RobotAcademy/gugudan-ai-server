from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.sql import func

from app.config.database.session import Base


class InquiryReplyModel(Base):
    __tablename__ = "inquiry_reply"

    id = Column(Integer, primary_key=True, autoincrement=True)
    inquiry_id = Column(Integer, ForeignKey("inquiry.id", ondelete="CASCADE"), nullable=False)
    account_id = Column(Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    is_admin_reply = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        Index('idx_inquiry_reply_inquiry', 'inquiry_id', 'created_at'),
    )

    def __repr__(self) -> str:
        return f"<InquiryReplyModel(id={self.id}, inquiry_id={self.inquiry_id}, is_admin={self.is_admin_reply})>"