from pydantic import BaseModel, Field
from typing import Optional


class SendMessageRequest(BaseModel):
    """메시지 전송 요청"""
    
    content: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="메시지 내용"
    )
    
    role: str = Field(
        default="USER",
        pattern="^(USER|ASSISTANT|SYSTEM)$",
        description="메시지 역할 (USER, ASSISTANT, SYSTEM)"
    )
    
    content_type: str = Field(
        default="TEXT",
        pattern="^(TEXT|IMAGE|FILE|SYSTEM)$",
        description="컨텐츠 타입 (TEXT, IMAGE, FILE, SYSTEM)"
    )
    
    img_url: Optional[str] = Field(
        default=None,
        max_length=500,
        description="이미지 URL (옵션)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "안녕하세요!",
                "role": "USER",
                "content_type": "TEXT"
            }
        }
