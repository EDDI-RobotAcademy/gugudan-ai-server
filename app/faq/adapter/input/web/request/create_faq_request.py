from typing import Optional
from pydantic import BaseModel, Field
from app.faq.domain.entity.faq_enums import FAQCategory


class CreateFAQRequest(BaseModel):
    category: FAQCategory = Field(..., description="FAQ 카테고리")
    question: str = Field(..., min_length=1, max_length=500, description="질문")
    answer: str = Field(..., min_length=1, description="답변")
    display_order: int = Field(0, ge=0, description="노출 순서")
    is_published: bool = Field(True, description="공개 여부")

    class Config:
        use_enum_values = True


class UpdateFAQRequest(BaseModel):

    category: Optional[FAQCategory] = Field(None, description="FAQ 카테고리")
    question: Optional[str] = Field(None, min_length=1, max_length=500, description="질문")
    answer: Optional[str] = Field(None, min_length=1, description="답변")
    display_order: Optional[int] = Field(None, ge=0, description="노출 순서")
    is_published: Optional[bool] = Field(None, description="공개 여부")

    class Config:
        use_enum_values = True