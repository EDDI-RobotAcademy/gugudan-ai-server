from abc import ABC, abstractmethod
from typing import Optional, List
from app.inquiry.domain.entity.inquiry import Inquiry
from app.inquiry.domain.entity.inquiry_enums import InquiryStatus


class InquiryRepositoryPort(ABC):
    @abstractmethod
    def save(self, inquiry: Inquiry) -> Inquiry:
        pass

    @abstractmethod
    def find_by_id(self, inquiry_id: int) -> Optional[Inquiry]:
        pass

    @abstractmethod
    def find_by_account_id(
        self,
        account_id: int,
        offset: int = 0,
        limit: int = 20
    ) -> List[Inquiry]:
        pass

    @abstractmethod
    def find_all(
        self,
        status: Optional[InquiryStatus] = None,
        offset: int = 0,
        limit: int = 20
    ) -> List[Inquiry]:
        pass

    @abstractmethod
    def delete(self, inquiry_id: int) -> bool:
        pass