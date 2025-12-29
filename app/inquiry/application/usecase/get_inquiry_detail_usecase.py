from typing import Dict
from app.inquiry.domain.exception import InquiryNotFoundException, InquiryAccessDeniedException
from app.inquiry.application.port.inquiry_repository_port import InquiryRepositoryPort
from app.inquiry.application.port.inquiry_reply_repository_port import InquiryReplyRepositoryPort


class GetInquiryDetailUseCase:
    def __init__(
        self,
        inquiry_repo: InquiryRepositoryPort,
        reply_repo: InquiryReplyRepositoryPort
    ):
        self.inquiry_repo = inquiry_repo
        self.reply_repo = reply_repo

    def execute(
        self,
        inquiry_id: int,
        account_id: int,
        is_admin: bool = False
    ) -> Dict[str, any]:
        # Find inquiry
        inquiry = self.inquiry_repo.find_by_id(inquiry_id)
        if not inquiry:
            raise InquiryNotFoundException(inquiry_id)

        # Check access permission
        if not is_admin and not inquiry.is_owned_by(account_id):
            raise InquiryAccessDeniedException(account_id, inquiry_id)

        # Get replies
        replies = self.reply_repo.find_by_inquiry_id(inquiry_id)

        return {
            "inquiry": inquiry,
            "replies": replies
        }