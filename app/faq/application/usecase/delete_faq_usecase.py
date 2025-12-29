from app.faq.domain.exception import FAQNotFoundException
from app.faq.application.port.faq_repository_port import FAQRepositoryPort


class DeleteFAQUseCase:
    def __init__(self, faq_repo: FAQRepositoryPort):
        self.faq_repo = faq_repo

    def execute(self, faq_id: int) -> bool:
        faq = self.faq_repo.find_by_id(faq_id)
        if not faq:
            raise FAQNotFoundException(faq_id)

        return self.faq_repo.delete(faq_id)