"""Withdraw account response schema."""

from pydantic import BaseModel


class WithdrawAccountResponse(BaseModel):
    """Response schema for account withdrawal."""

    message: str
    account_id: int

    class Config:
        from_attributes = True
