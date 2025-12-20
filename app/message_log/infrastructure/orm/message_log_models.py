from sqlalchemy import (
    Column, Integer, String, DateTime, Enum as SQLEnum,
    ForeignKey, LargeBinary, SmallInteger, Boolean
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

from app.config.database.session import Base



# Enum 정의
class MessageRoleEnum(str, enum.Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"


class ContentTypeEnum(str, enum.Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    FILE = "FILE"
    SYSTEM = "SYSTEM"


class ChatRoomModel(Base):
    """채팅방 ORM 모델"""
    __tablename__ = "chat_room"

    id = Column(String(36), primary_key=True)
    account_id = Column(
        Integer,
        ForeignKey("account.id", ondelete="CASCADE"),
        nullable=False
    )
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationships
    messages = relationship(
        "ChatMessageModel",
        back_populates="room",
        cascade="all, delete-orphan"
    )


class ChatMessageModel(Base):
    """채팅 메시지 ORM 모델 (암호화됨)"""
    __tablename__ = "chat_message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_room_id = Column(
        String(36),
        ForeignKey("chat_room.id", ondelete="CASCADE"),
        nullable=False
    )
    account_id = Column(
        Integer,
        ForeignKey("account.id", ondelete="CASCADE"),
        nullable=False
    )
    role = Column(SQLEnum(MessageRoleEnum), nullable=False)

    # GS-8: 암호화 필드
    content_enc = Column(LargeBinary, nullable=False)  # 암호화된 메시지
    iv = Column(LargeBinary(16), nullable=False)  # 암호화 벡터
    enc_version = Column(SmallInteger, nullable=False, default=1)  # 암호화 버전

    contents_type = Column(SQLEnum(ContentTypeEnum), nullable=False, default=ContentTypeEnum.TEXT)
    img_url = Column(String(500), nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    room = relationship("ChatRoomModel", back_populates="messages")

    def __repr__(self):
        """보안: 암호화된 내용은 출력하지 않음"""
        return (
            f"<ChatMessageModel(id={self.id}, "
            f"room_id={self.chat_room_id}, "
            f"role={self.role}, "
            f"enc_version={self.enc_version})>"
        )


# Base 메타데이터 생성
def init_db(engine):
    """DB 초기화 (테이블 생성)"""
    Base.metadata.create_all(bind=engine)