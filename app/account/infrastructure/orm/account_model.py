"""SQLAlchemy ORM model for Account."""

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.config.database.session import Base


class AccountModel(Base):
    """SQLAlchemy model for the account table.

    Maps to the domain Account entity for persistence.
    """

    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    nickname = Column(String(100), nullable=False)
    terms_agreed = Column(Boolean, default=False, nullable=False)
    terms_agreed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    # New columns
    role = Column(String(30), default="USER", nullable=False)
    plan = Column(String(30), default="FREE", nullable=False)
    plan_started_at = Column(DateTime, nullable=True)
    plan_ends_at = Column(DateTime, nullable=True)
    billing_customer_id = Column(String(100), nullable=True)
    mbti = Column(String(4), nullable=True)
    gender = Column(String(10), nullable=True)
    status = Column(String(30), default="ACTIVE", nullable=False)

    def __repr__(self) -> str:
        return f"<AccountModel(id={self.id}, email={self.email}, role={self.role}, plan={self.plan}, status={self.status})>"
