from datetime import datetime
from pydantic import BaseModel

from app.faq.domain.entity.faq_enums import FAQCategory


class FAQResponse(BaseModel):
    id: int
    category: FAQCategory
    question: str
    answer: str
    display_order: int
    is_published: bool
    view_count: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True