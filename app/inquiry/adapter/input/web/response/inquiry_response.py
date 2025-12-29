from datetime import datetime
from typing import List
from pydantic import BaseModel

from app.inquiry.domain.entity.inquiry_enums import InquiryStatus, InquiryCategory


class InquiryReplyResponse(BaseModel):
    id: int
    inquiry_id: int
    account_id: int
    content: str
    is_admin_reply: bool
    created_at: datetime

    class Config:
        from_attributes = True


class InquiryResponse(BaseModel):
    id: int
    account_id: int
    category: InquiryCategory
    title: str
    content: str
    status: InquiryStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True


class InquiryDetailResponse(BaseModel):
    inquiry: InquiryResponse
    replies: List[InquiryReplyResponse]

    class Config:
        from_attributes = True