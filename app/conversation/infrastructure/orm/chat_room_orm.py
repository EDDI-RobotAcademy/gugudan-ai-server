from sqlalchemy import Column, String, Integer, DateTime, Index
from sqlalchemy.orm import relationship

from app.config.database.session import Base
from datetime import datetime


class ChatRoomOrm(Base):
    __tablename__ = "chat_room"

    room_id = Column(String(36), primary_key=True)
    account_id = Column(Integer, nullable=False)
    title = Column(String(100))
    category = Column(String(20))
    division = Column(String(20))
    out_api = Column(String(50))
    status = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship(
        "ChatMessageOrm",
        backref="room",
        cascade="all, delete-orphan",
        passive_deletes=True  # DB의 ON DELETE CASCADE 기능을 활용함
    )

    __table_args__ = (
            # 1. 내 채팅방 목록 조회 최적화
            Index('idx_account_updated', 'account_id', 'updated_at'),

            # 2. 특정 카테고리나 상태(ACTIVE)별로 필터링해서 볼 경우
            Index('idx_status_category', 'status', 'category'),
        )