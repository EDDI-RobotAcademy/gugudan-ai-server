from typing import Optional
from app.faq.domain.entity.faq import FAQ
from app.faq.domain.entity.faq_enums import FAQCategory
from app.faq.domain.exception import FAQNotFoundException
from app.faq.application.port.faq_repository_port import FAQRepositoryPort


class UpdateFAQUseCase:
    def __init__(self, faq_repo: FAQRepositoryPort):
        self.faq_repo = faq_repo

    def execute(
        self,
        faq_id: int,
        category: Optional[FAQCategory] = None,
        question: Optional[str] = None,
        answer: Optional[str] = None,
        display_order: Optional[int] = None,
        is_published: Optional[bool] = None
    ) -> FAQ:
        faq = self.faq_repo.find_by_id(faq_id)
        if not faq:
            raise FAQNotFoundException(faq_id)

        if category is not None or question is not None or answer is not None:
            faq.update_content(
                question=question or faq.question,
                answer=answer or faq.answer,
                category=category or faq.category
            )

        if display_order is not None:
            faq.update_order(display_order)

        if is_published is not None:
            if is_published:
                faq.publish()
            else:
                faq.unpublish()

        return self.faq_repo.save(faq)