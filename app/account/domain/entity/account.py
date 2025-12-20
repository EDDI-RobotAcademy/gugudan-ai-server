"""Account entity - Domain model for user accounts."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.account.domain.entity.account_enums import (
    AccountPlan,
    AccountRole,
    AccountStatus, Gender, Mbti,
)


@dataclass
class Account:
    """Domain entity representing a user account.

    This is a pure domain object with no framework dependencies.
    """

    email: str
    nickname: str
    id: Optional[int] = None
    terms_agreed: bool = False
    terms_agreed_at: Optional[datetime] = None
    created_at: Optional[datetime] = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = field(default_factory=datetime.now)
    # New fields
    role: AccountRole = AccountRole.USER
    plan: AccountPlan = AccountPlan.FREE
    plan_started_at: Optional[datetime] = None
    plan_ends_at: Optional[datetime] = None
    billing_customer_id: Optional[str] = None
    gender: Optional[Gender] = None
    mbti: Optional[Mbti] = None
    status: AccountStatus = AccountStatus.ACTIVE

    def __post_init__(self):
        """Validate entity on creation."""
        if not self.email:
            raise ValueError("Email is required")
        if not self.nickname:
            raise ValueError("Nickname is required")
        if "@" not in self.email:
            raise ValueError("Invalid email format")
        # Convert string values to enums if necessary
        if isinstance(self.role, str):
            self.role = AccountRole.from_string(self.role)
        if isinstance(self.plan, str):
            self.plan = AccountPlan.from_string(self.plan)
        if isinstance(self.status, str):
            self.status = AccountStatus.from_string(self.status)

    def agree_to_terms(self) -> None:
        """Mark that user has agreed to terms of service."""
        self.terms_agreed = True
        self.terms_agreed_at = datetime.now()
        self.updated_at = datetime.now()

    def update_nickname(self, nickname: str) -> None:
        """Update the user's nickname."""
        if not nickname:
            raise ValueError("Nickname cannot be empty")
        self.nickname = nickname
        self.updated_at = datetime.now()

    def is_new(self) -> bool:
        """Check if this is a new account (not yet persisted)."""
        return self.id is None

    def is_active(self) -> bool:
        """Check if the account is active."""
        return self.status == AccountStatus.ACTIVE

    def is_admin(self) -> bool:
        """Check if the user has admin role."""
        return self.role == AccountRole.ADMIN

    def has_paid_plan(self) -> bool:
        """Check if the user has a paid subscription plan."""
        return self.plan in (AccountPlan.PRO, AccountPlan.TEAM)

    def is_plan_expired(self) -> bool:
        """Check if the subscription plan has expired."""
        if self.plan == AccountPlan.FREE:
            return False
        if self.plan_ends_at is None:
            return False
        return datetime.now() > self.plan_ends_at

    def upgrade_plan(self, plan: AccountPlan, ends_at: Optional[datetime] = None) -> None:
        """Upgrade the user's subscription plan.

        Args:
            plan: The new plan to upgrade to.
            ends_at: When the plan expires (None for indefinite).
        """
        self.plan = plan
        self.plan_started_at = datetime.now()
        self.plan_ends_at = ends_at
        self.updated_at = datetime.now()

    def downgrade_to_free(self) -> None:
        """Downgrade the user to free plan."""
        self.plan = AccountPlan.FREE
        self.plan_started_at = datetime.now()
        self.plan_ends_at = None
        self.updated_at = datetime.now()

    def suspend(self) -> None:
        """Suspend the account."""
        self.status = AccountStatus.SUSPENDED
        self.updated_at = datetime.now()

    def activate(self) -> None:
        """Activate the account."""
        self.status = AccountStatus.ACTIVE
        self.updated_at = datetime.now()

    def soft_delete(self) -> None:
        """Soft delete the account."""
        self.status = AccountStatus.DELETED
        self.updated_at = datetime.now()

    def set_billing_customer_id(self, customer_id: str) -> None:
        """Set the billing customer ID from payment provider.

        Args:
            customer_id: The customer ID from the payment provider (e.g., Toss).
        """
        self.billing_customer_id = customer_id
        self.updated_at = datetime.now()

    def promote_to_admin(self) -> None:
        """Promote the user to admin role."""
        self.role = AccountRole.ADMIN
        self.updated_at = datetime.now()

    def demote_to_user(self) -> None:
        """Demote the admin to regular user role."""
        self.role = AccountRole.USER
        self.updated_at = datetime.now()
