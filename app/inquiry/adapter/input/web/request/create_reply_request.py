from pydantic import BaseModel, Field


class CreateReplyRequest(BaseModel):
    content: str = Field(..., min_length=1, description="답변 내용")