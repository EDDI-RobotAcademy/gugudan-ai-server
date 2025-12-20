from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessageResponse(BaseModel):
    """메시지 응답"""
    
    message_id: int = Field(..., description="메시지 ID")
    chat_room_id: str = Field(..., description="채팅방 ID")
    account_id: int = Field(..., description="사용자 ID")
    role: str = Field(..., description="메시지 역할")
    content_type: str = Field(..., description="컨텐츠 타입")
    img_url: Optional[str] = Field(None, description="이미지 URL")
    created_at: datetime = Field(..., description="생성 시각")
    
    # ⚠️ 보안: 원본 내용(content_enc)은 반환하지 않음!
    
    class Config:
        json_schema_extra = {
            "example": {
                "message_id": 123,
                "chat_room_id": "room-abc-123",
                "account_id": 1,
                "role": "USER",
                "content_type": "TEXT",
                "img_url": None,
                "created_at": "2024-01-01T12:00:00"
            }
        }


class MessageListResponse(BaseModel):
    """메시지 목록 응답"""
    
    messages: list[MessageResponse] = Field(..., description="메시지 목록")
    total_count: int = Field(..., description="전체 메시지 개수")
    limit: int = Field(..., description="조회 개수")
    offset: int = Field(..., description="오프셋")
    
    class Config:
        json_schema_extra = {
            "example": {
                "messages": [],
                "total_count": 100,
                "limit": 50,
                "offset": 0
            }
        }
