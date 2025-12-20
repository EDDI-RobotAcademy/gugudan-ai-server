from typing import List, Optional, Tuple

from app.message_log.domain.entity import ChatMessage
from app.message_log.infrastructure.repository.chat_message_repository_impl import ChatMessageRepositoryImpl
from app.config.security.message_crypto import AESEncryption


class GetMessagesUseCase:
    """메시지 조회 UseCase"""

    def __init__(self):
        self.message_repo = ChatMessageRepositoryImpl()
        self.encryption = AESEncryption()

    def get_by_room_id(
        self,
        room_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[ChatMessage], int]:
        """
        채팅방의 메시지 목록 조회

        Args:
            room_id: 채팅방 ID
            limit: 조회 개수
            offset: 오프셋

        Returns:
            (메시지 목록, 전체 개수)
        """
        messages = self.message_repo.find_by_room_id(room_id, limit, offset)
        total_count = self.message_repo.count_by_room_id(room_id)

        return messages, total_count

    def get_by_id(self, message_id: int) -> Optional[ChatMessage]:
        """
        ID로 메시지 조회

        Args:
            message_id: 메시지 ID

        Returns:
            ChatMessage 또는 None
        """
        return self.message_repo.find_by_id(message_id)

    def count_by_room_id(self, room_id: str) -> int:
        """
        채팅방의 메시지 개수 조회

        Args:
            room_id: 채팅방 ID

        Returns:
            메시지 개수
        """
        return self.message_repo.count_by_room_id(room_id)

    def decrypt_message(self, message: ChatMessage) -> str:
        """
        메시지 복호화

        Args:
            message: 암호화된 메시지

        Returns:
            원본 메시지 내용
        """
        return self.encryption.decrypt(message.content_enc, message.iv)