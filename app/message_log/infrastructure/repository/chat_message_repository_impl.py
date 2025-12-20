"""
채팅 메시지 레포지토리 구현 (동기 버전)
"""
from typing import List, Optional

from app.message_log.application.port.chat_message_repository_port import ChatMessageRepositoryPort
from app.message_log.domain.entity import ChatMessage, MessageRole, ContentType
from app.message_log.infrastructure.orm.message_log_models import (
    ChatMessageModel,
    MessageRoleEnum,
    ContentTypeEnum
)
from app.config.database.session import SessionLocal


class ChatMessageRepositoryImpl(ChatMessageRepositoryPort):
    """채팅 메시지 레포지토리 구현"""

    def __init__(self):
        self.db = SessionLocal()

    def save(self, message: ChatMessage) -> ChatMessage:
        """메시지 저장"""
        model = self._to_model(message)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return self._to_entity(model)

    def find_by_id(self, message_id: int) -> Optional[ChatMessage]:
        """ID로 메시지 조회"""
        model = self.db.query(ChatMessageModel).filter(
            ChatMessageModel.id == message_id
        ).first()

        return self._to_entity(model) if model else None

    def find_by_room_id(
            self,
            room_id: str,
            limit: int = 50,
            offset: int = 0
    ) -> List[ChatMessage]:
        """채팅방의 메시지 목록 조회"""
        models = self.db.query(ChatMessageModel).filter(
            ChatMessageModel.chat_room_id == room_id
        ).order_by(
            ChatMessageModel.created_at.desc()
        ).limit(limit).offset(offset).all()

        return [self._to_entity(model) for model in models]

    def count_by_room_id(self, room_id: str) -> int:
        """채팅방의 메시지 개수"""
        return self.db.query(ChatMessageModel).filter(
            ChatMessageModel.chat_room_id == room_id
        ).count()

    def delete_by_id(self, message_id: int) -> bool:
        """메시지 삭제"""
        model = self.db.query(ChatMessageModel).filter(
            ChatMessageModel.id == message_id
        ).first()

        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False

    @staticmethod
    def _to_model(entity: ChatMessage) -> ChatMessageModel:
        """Domain Entity → ORM Model 변환"""
        model = ChatMessageModel()

        if entity.id != 0:
            model.id = entity.id

        model.chat_room_id = entity.chat_room_id
        model.account_id = entity.account_id
        model.role = MessageRoleEnum[entity.role.value]
        model.content_enc = entity.content_enc
        model.iv = entity.iv
        model.enc_version = entity.enc_version
        model.contents_type = ContentTypeEnum[entity.contents_type.value]
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        model.img_url = entity.img_url

        return model

    @staticmethod
    def _to_entity(model: ChatMessageModel) -> ChatMessage:
        """ORM Model → Domain Entity 변환"""
        return ChatMessage(
            id=model.id,
            chat_room_id=model.chat_room_id,
            account_id=model.account_id,
            role=MessageRole[model.role.value],
            content_enc=model.content_enc,
            iv=model.iv,
            enc_version=model.enc_version,
            contents_type=ContentType[model.contents_type.value],
            created_at=model.created_at,
            updated_at=model.updated_at,
            img_url=model.img_url
        )