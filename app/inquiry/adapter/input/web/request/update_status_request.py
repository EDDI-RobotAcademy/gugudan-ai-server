from pydantic import BaseModel, Field
from app.inquiry.domain.entity.inquiry_enums import InquiryStatus


class UpdateStatusRequest(BaseModel):
    status: InquiryStatus = Field(..., description="새로운 상태")

    class Config:
        use_enum_values = True