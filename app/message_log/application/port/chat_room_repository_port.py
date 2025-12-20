from abc import ABC, abstractmethod
from typing import List, Optional
from app.message_log.domain.entity import ChatRoom


class ChatRoomRepositoryPort(ABC):
    """채팅방 레포지토리 인터페이스"""
    
    @abstractmethod
    async def save(self, room: ChatRoom) -> ChatRoom:
        """
        채팅방 저장
        
        Args:
            room: 저장할 채팅방 엔티티
            
        Returns:
            ChatRoom: 저장된 채팅방
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, room_id: str) -> Optional[ChatRoom]:
        """
        ID로 채팅방 조회
        
        Args:
            room_id: 채팅방 ID
            
        Returns:
            Optional[ChatRoom]: 채팅방 또는 None
        """
        pass
    
    @abstractmethod
    async def find_by_account_id(self, account_id: int) -> List[ChatRoom]:
        """
        사용자의 채팅방 목록 조회
        
        Args:
            account_id: 사용자 ID
            
        Returns:
            List[ChatRoom]: 채팅방 목록
        """
        pass
    
    @abstractmethod
    async def delete_by_id(self, room_id: str) -> bool:
        """
        채팅방 삭제 (CASCADE로 메시지도 삭제됨)
        
        Args:
            room_id: 삭제할 채팅방 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        pass
