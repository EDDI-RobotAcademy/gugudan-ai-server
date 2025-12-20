from abc import ABC, abstractmethod
from typing import List, Optional
from app.message_log.domain.entity import ChatMessage


class ChatMessageRepositoryPort(ABC):
    """채팅 메시지 레포지토리 인터페이스"""
    
    @abstractmethod
    async def save(self, message: ChatMessage) -> ChatMessage:
        """
        메시지 저장
        
        Args:
            message: 저장할 메시지 엔티티
            
        Returns:
            ChatMessage: 저장된 메시지 (ID 포함)
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, message_id: int) -> Optional[ChatMessage]:
        """
        ID로 메시지 조회
        
        Args:
            message_id: 메시지 ID
            
        Returns:
            Optional[ChatMessage]: 메시지 또는 None
        """
        pass
    
    @abstractmethod
    async def find_by_room_id(
        self, 
        room_id: str, 
        limit: int = 50,
        offset: int = 0
    ) -> List[ChatMessage]:
        """
        채팅방의 메시지 목록 조회
        
        Args:
            room_id: 채팅방 ID
            limit: 최대 조회 개수
            offset: 오프셋
            
        Returns:
            List[ChatMessage]: 메시지 목록
        """
        pass
    
    @abstractmethod
    async def count_by_room_id(self, room_id: str) -> int:
        """
        채팅방의 메시지 개수
        
        Args:
            room_id: 채팅방 ID
            
        Returns:
            int: 메시지 개수
        """
        pass
    
    @abstractmethod
    async def delete_by_id(self, message_id: int) -> bool:
        """
        메시지 삭제
        
        Args:
            message_id: 삭제할 메시지 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        pass
