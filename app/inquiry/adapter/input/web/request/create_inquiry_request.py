from pydantic import BaseModel, Field
from app.inquiry.domain.entity.inquiry_enums import InquiryCategory


class CreateInquiryRequest(BaseModel):
    category: InquiryCategory = Field(..., description="문의 카테고리")
    title: str = Field(..., min_length=1, max_length=100, description="문의 제목")
    content: str = Field(..., min_length=1, description="문의 내용")

    class Config:
        use_enum_values = True