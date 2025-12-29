from abc import ABC, abstractmethod
from typing import Optional, List
from app.inquiry.domain.entity.inquiry_reply import InquiryReply


class InquiryReplyRepositoryPort(ABC):
    @abstractmethod
    def save(self, reply: InquiryReply) -> InquiryReply:
        pass

    @abstractmethod
    def find_by_id(self, reply_id: int) -> Optional[InquiryReply]:
        pass

    @abstractmethod
    def find_by_inquiry_id(self, inquiry_id: int) -> List[InquiryReply]:
        pass

    @abstractmethod
    def delete(self, reply_id: int) -> bool:
        pass