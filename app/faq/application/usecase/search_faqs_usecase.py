from typing import List
from app.faq.domain.entity.faq import FAQ
from app.faq.application.port.faq_repository_port import FAQRepositoryPort


class SearchFAQsUseCase:
    def __init__(self, faq_repo: FAQRepositoryPort):
        self.faq_repo = faq_repo

    def execute(
        self,
        keyword: str,
        offset: int = 0,
        limit: int = 20
    ) -> List[FAQ]:
        return self.faq_repo.search(
            keyword=keyword,
            offset=offset,
            limit=limit
        )