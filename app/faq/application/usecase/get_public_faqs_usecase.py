from typing import List, Optional
from app.faq.domain.entity.faq import FAQ
from app.faq.domain.entity.faq_enums import FAQCategory
from app.faq.application.port.faq_repository_port import FAQRepositoryPort


class GetPublicFAQsUseCase:
    def __init__(self, faq_repo: FAQRepositoryPort):
        self.faq_repo = faq_repo

    def execute(
        self,
        category: Optional[FAQCategory] = None,
        offset: int = 0,
        limit: int = 20
    ) -> List[FAQ]:
        return self.faq_repo.find_published(
            category=category,
            offset=offset,
            limit=limit
        )