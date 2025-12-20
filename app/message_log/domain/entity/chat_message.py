from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class MessageRole(str, Enum):
    """메시지 역할"""
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"


class ContentType(str, Enum):
    """컨텐츠 타입"""
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    FILE = "FILE"
    SYSTEM = "SYSTEM"


@dataclass
class ChatMessage:
    """
    채팅 메시지 엔티티 (Aggregate Root)
    
    보안 정책 (GS-8):
    - content_enc: 암호화된 원본 메시지
    - iv: 암호화 벡터
    - 원본 내용은 절대 로그/출력하지 않음
    """
    id: int
    chat_room_id: str
    account_id: int
    role: MessageRole
    content_enc: bytes  # 암호화된 메시지
    iv: bytes  # AES IV
    enc_version: int  # 암호화 버전
    contents_type: ContentType
    created_at: datetime = None  # 기본값 추가
    updated_at: datetime = None  # 기본값 추가
    img_url: Optional[str] = None

    def __post_init__(self):
        """생성 시 자동으로 시간 설정"""
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """보안: 암호화된 내용은 출력하지 않음"""
        return (
            f"ChatMessage("
            f"id={self.id}, "
            f"room={self.chat_room_id}, "
            f"role={self.role.value}, "
            f"type={self.contents_type.value})"
        )

    def __str__(self) -> str:
        """보안: 문자열 변환 시에도 내용 노출 방지"""
        return self.__repr__()

    def is_user_message(self) -> bool:
        """사용자 메시지 여부"""
        return self.role == MessageRole.USER

    def is_assistant_message(self) -> bool:
        """어시스턴트 메시지 여부"""
        return self.role == MessageRole.ASSISTANT

    def has_image(self) -> bool:
        """이미지 포함 여부"""
        return self.img_url is not None