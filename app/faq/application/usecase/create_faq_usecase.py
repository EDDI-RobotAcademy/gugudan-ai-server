from app.faq.domain.entity.faq import FAQ
from app.faq.domain.entity.faq_enums import FAQCategory
from app.faq.application.port.faq_repository_port import FAQRepositoryPort


class CreateFAQUseCase:
    def __init__(self, faq_repo: FAQRepositoryPort):
        self.faq_repo = faq_repo

    def execute(
        self,
        category: FAQCategory,
        question: str,
        answer: str,
        created_by: int,
        display_order: int = 0,
        is_published: bool = True
    ) -> FAQ:
        faq = FAQ(
            category=category,
            question=question,
            answer=answer,
            created_by=created_by,
            display_order=display_order,
            is_published=is_published,
        )

        return self.faq_repo.save(faq)