from typing import List, Optional
from app.inquiry.domain.entity.inquiry import Inquiry
from app.inquiry.domain.entity.inquiry_enums import InquiryStatus
from app.inquiry.application.port.inquiry_repository_port import InquiryRepositoryPort


class GetAllInquiriesUseCase:
    def __init__(self, inquiry_repo: InquiryRepositoryPort):
        self.inquiry_repo = inquiry_repo

    def execute(
        self,
        status: Optional[InquiryStatus] = None,
        offset: int = 0,
        limit: int = 20
    ) -> List[Inquiry]:
        return self.inquiry_repo.find_all(
            status=status,
            offset=offset,
            limit=limit
        )