"""Auth API schemas - Pydantic models for request/response."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.domain.account.entity import Account


class UserResponse(BaseModel):
    """Response schema for user/account data."""

    id: int
    email: EmailStr
    nickname: str
    terms_agreed: bool
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_entity(cls, account: Account) -> "UserResponse":
        """Create response from domain entity."""
        return cls(
            id=account.id,
            email=account.email,
            nickname=account.nickname,
            terms_agreed=account.terms_agreed,
            created_at=account.created_at,
        )


class AuthStatusResponse(BaseModel):
    """Response for authentication status check."""

    is_authenticated: bool
    user: Optional[UserResponse] = None


class LogoutResponse(BaseModel):
    """Response for logout endpoint."""

    message: str = "Logged out successfully"


class OAuthProvidersResponse(BaseModel):
    """Response listing supported OAuth providers."""

    providers: list[str]


class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str
    code: Optional[str] = None
