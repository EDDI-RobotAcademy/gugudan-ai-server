from datetime import datetime
from typing import Optional
from app.faq.domain.entity.faq_enums import FAQCategory


class FAQ:
    def __init__(
        self,
        category: FAQCategory,
        question: str,
        answer: str,
        created_by: int,
        id: Optional[int] = None,
        display_order: int = 0,
        is_published: bool = True,
        view_count: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.category = category
        self.question = question
        self.answer = answer
        self.display_order = display_order
        self.is_published = is_published
        self.view_count = view_count
        self.created_by = created_by
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def publish(self) -> None:
        self.is_published = True
        self.updated_at = datetime.utcnow()

    def unpublish(self) -> None:
        self.is_published = False
        self.updated_at = datetime.utcnow()

    def update_order(self, new_order: int) -> None:
        self.display_order = new_order
        self.updated_at = datetime.utcnow()

    def increment_view_count(self) -> None:
        self.view_count += 1

    def update_content(self, question: str, answer: str, category: FAQCategory) -> None:
        self.question = question
        self.answer = answer
        self.category = category
        self.updated_at = datetime.utcnow()