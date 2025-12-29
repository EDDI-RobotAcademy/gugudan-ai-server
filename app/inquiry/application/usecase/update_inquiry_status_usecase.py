from app.inquiry.domain.entity.inquiry import Inquiry
from app.inquiry.domain.entity.inquiry_enums import InquiryStatus
from app.inquiry.domain.exception import InquiryNotFoundException
from app.inquiry.application.port.inquiry_repository_port import InquiryRepositoryPort


class UpdateInquiryStatusUseCase:
    def __init__(self, inquiry_repo: InquiryRepositoryPort):
        self.inquiry_repo = inquiry_repo

    def execute(
        self,
        inquiry_id: int,
        new_status: InquiryStatus
    ) -> Inquiry:
        inquiry = self.inquiry_repo.find_by_id(inquiry_id)
        if not inquiry:
            raise InquiryNotFoundException(inquiry_id)

        inquiry.update_status(new_status)

        return self.inquiry_repo.save(inquiry)