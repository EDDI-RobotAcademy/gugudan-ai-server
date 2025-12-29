from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.sql import func

from app.config.database.session import Base


class FAQModel(Base):
    __tablename__ = "faq"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(30), nullable=False)
    question = Column(String(500), nullable=False)
    answer = Column(Text, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    created_by = Column(Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index('idx_faq_category_order', 'category', 'display_order'),
        Index('idx_faq_published', 'is_published', 'display_order'),
    )

    def __repr__(self) -> str:
        return f"<FAQModel(id={self.id}, category={self.category}, is_published={self.is_published})>"