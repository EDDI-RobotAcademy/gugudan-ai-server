"""Account-related enumerations."""

from enum import Enum


class AccountRole(str, Enum):
    """User role enumeration.

    Defines the permission levels for users in the system.
    """

    USER = "USER"
    ADMIN = "ADMIN"

    @classmethod
    def from_string(cls, role: str) -> "AccountRole":
        """Convert a string to AccountRole.

        Args:
            role: The role name string.

        Returns:
            The corresponding AccountRole.

        Raises:
            ValueError: If role is not valid.
        """
        role_upper = role.upper()
        for r in cls:
            if r.value == role_upper:
                return r
        raise ValueError(f"Invalid role: {role}")


class AccountPlan(str, Enum):
    """Subscription plan enumeration.

    Defines the available subscription tiers.
    """

    FREE = "FREE"
    PRO = "PRO"
    TEAM = "TEAM"

    @classmethod
    def from_string(cls, plan: str) -> "AccountPlan":
        """Convert a string to AccountPlan.

        Args:
            plan: The plan name string.

        Returns:
            The corresponding AccountPlan.

        Raises:
            ValueError: If plan is not valid.
        """
        plan_upper = plan.upper()
        for p in cls:
            if p.value == plan_upper:
                return p
        raise ValueError(f"Invalid plan: {plan}")


class AccountStatus(str, Enum):
    """Account status enumeration.

    Defines the possible states of a user account.
    """

    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"

    @classmethod
    def from_string(cls, status: str) -> "AccountStatus":
        """Convert a string to AccountStatus.

        Args:
            status: The status name string.

        Returns:
            The corresponding AccountStatus.

        Raises:
            ValueError: If status is not valid.
        """
        status_upper = status.upper()
        for s in cls:
            if s.value == status_upper:
                return s
        raise ValueError(f"Invalid status: {status}")

    def is_active(self) -> bool:
        """Check if the status allows normal account operations."""
        return self == AccountStatus.ACTIVE

class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

    @classmethod
    def from_string(cls, v: str) -> "Gender":
        return cls[v.upper()] if v.upper() in cls.__members__ else cls(v.upper())

class Mbti(Enum):
    ISTJ = "ISTJ"
    ISFJ = "ISFJ"
    INFJ = "INFJ"
    INTJ = "INTJ"
    ISTP = "ISTP"
    ISFP = "ISFP"
    INFP = "INFP"
    INTP = "INTP"
    ESTP = "ESTP"
    ESFP = "ESFP"
    ENFP = "ENFP"
    ENTP = "ENTP"
    ESTJ = "ESTJ"
    ESFJ = "ESFJ"
    ENFJ = "ENFJ"
    ENTJ = "ENTJ"

    @classmethod
    def from_string(cls, value: str) -> "Mbti":
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid MBTI value: {value}")
