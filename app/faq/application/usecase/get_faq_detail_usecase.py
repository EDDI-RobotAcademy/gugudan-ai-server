from app.faq.domain.entity.faq import FAQ
from app.faq.domain.exception import FAQNotFoundException
from app.faq.application.port.faq_repository_port import FAQRepositoryPort


class GetFAQDetailUseCase:
    def __init__(self, faq_repo: FAQRepositoryPort):
        self.faq_repo = faq_repo

    def execute(self, faq_id: int, increment_view: bool = True) -> FAQ:
        # Find FAQ
        faq = self.faq_repo.find_by_id(faq_id)
        if not faq:
            raise FAQNotFoundException(faq_id)

        # Increment view count if requested
        if increment_view:
            self.faq_repo.increment_view_count(faq_id)
            faq.increment_view_count()

        return faq