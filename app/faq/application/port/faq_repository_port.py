from abc import ABC, abstractmethod
from typing import Optional, List
from app.faq.domain.entity.faq import FAQ
from app.faq.domain.entity.faq_enums import FAQCategory


class FAQRepositoryPort(ABC):
    @abstractmethod
    def save(self, faq: FAQ) -> FAQ:
        pass

    @abstractmethod
    def find_by_id(self, faq_id: int) -> Optional[FAQ]:
        pass

    @abstractmethod
    def find_published(
        self,
        category: Optional[FAQCategory] = None,
        offset: int = 0,
        limit: int = 20
    ) -> List[FAQ]:
        pass

    @abstractmethod
    def search(
        self,
        keyword: str,
        offset: int = 0,
        limit: int = 20
    ) -> List[FAQ]:
        pass

    @abstractmethod
    def find_all(
        self,
        offset: int = 0,
        limit: int = 20
    ) -> List[FAQ]:
        pass

    @abstractmethod
    def increment_view_count(self, faq_id: int) -> bool:
        pass

    @abstractmethod
    def delete(self, faq_id: int) -> bool:
        pass