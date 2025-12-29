from typing import List
from app.inquiry.domain.entity.inquiry import Inquiry
from app.inquiry.application.port.inquiry_repository_port import InquiryRepositoryPort


class GetMyInquiriesUseCase:
    def __init__(self, inquiry_repo: InquiryRepositoryPort):
        self.inquiry_repo = inquiry_repo

    def execute(
        self,
        account_id: int,
        offset: int = 0,
        limit: int = 20
    ) -> List[Inquiry]:
        return self.inquiry_repo.find_by_account_id(
            account_id=account_id,
            offset=offset,
            limit=limit
        )