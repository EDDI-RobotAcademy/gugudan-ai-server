from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatRoom:
    """
    채팅방 엔티티 (Aggregate Root)
    """
    id: str
    account_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    def __repr__(self) -> str:
        return f"ChatRoom(id={self.id}, account_id={self.account_id}, title={self.title})"
    
    def deactivate(self) -> None:
        """채팅방 비활성화"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """채팅방 활성화"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def update_title(self, new_title: str) -> None:
        """제목 변경"""
        self.title = new_title
        self.updated_at = datetime.utcnow()
