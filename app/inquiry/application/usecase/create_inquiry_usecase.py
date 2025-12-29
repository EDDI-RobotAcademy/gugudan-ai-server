from app.inquiry.domain.entity.inquiry import Inquiry
from app.inquiry.domain.entity.inquiry_enums import InquiryCategory
from app.inquiry.application.port.inquiry_repository_port import InquiryRepositoryPort


class CreateInquiryUseCase:
    def __init__(self, inquiry_repo: InquiryRepositoryPort):
        self.inquiry_repo = inquiry_repo

    def execute(
        self,
        account_id: int,
        category: InquiryCategory,
        title: str,
        content: str
    ) -> Inquiry:
        inquiry = Inquiry(
            account_id=account_id,
            category=category,
            title=title,
            content=content,
        )

        return self.inquiry_repo.save(inquiry)