from typing import List, Optional

from app.message_log.domain.entity import ChatMessage
from app.message_log.application.port.chat_message_repository_port import ChatMessageRepositoryPort
from app.message_log.application.port.encryption_port import EncryptionPort


class GetMessagesUseCase:
    """
    메시지 조회 UseCase

    책임:
    1. 채팅방의 메시지 목록 조회
    2. 필요 시 복호화
    """

    def __init__(
            self,
            message_repository: ChatMessageRepositoryPort,
            encryption: EncryptionPort
    ):
        self.message_repository = message_repository
        self.encryption = encryption

    async def get_by_room_id(
            self,
            room_id: str,
            limit: int = 50,
            offset: int = 0,
            decrypt: bool = False
    ) -> List[ChatMessage]:
        """
        채팅방의 메시지 목록 조회

        Args:
            room_id: 채팅방 ID
            limit: 최대 조회 개수
            offset: 오프셋
            decrypt: 복호화 여부 (기본값: False)

        Returns:
            List[ChatMessage]: 메시지 목록
        """
        messages = await self.message_repository.find_by_room_id(
            room_id=room_id,
            limit=limit,
            offset=offset
        )

        # 복호화는 필요 시에만
        # (일반적으로는 암호화된 상태로 반환)
        return messages

    async def get_by_id(
            self,
            message_id: int,
            decrypt: bool = False
    ) -> Optional[ChatMessage]:
        """
        ID로 메시지 조회

        Args:
            message_id: 메시지 ID
            decrypt: 복호화 여부

        Returns:
            Optional[ChatMessage]: 메시지 또는 None
        """
        message = await self.message_repository.find_by_id(message_id)
        return message

    async def count_by_room_id(self, room_id: str) -> int:
        """
        채팅방의 메시지 개수

        Args:
            room_id: 채팅방 ID

        Returns:
            int: 메시지 개수
        """
        return await self.message_repository.count_by_room_id(room_id)

    def decrypt_message(self, message: ChatMessage) -> str:
        """
        메시지 복호화

        Args:
            message: 암호화된 메시지

        Returns:
            str: 복호화된 내용
        """
        return self.encryption.decrypt(message.content_enc)