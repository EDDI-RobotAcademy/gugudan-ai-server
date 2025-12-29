from app.inquiry.domain.entity.inquiry_reply import InquiryReply
from app.inquiry.domain.exception import InquiryNotFoundException
from app.inquiry.application.port.inquiry_repository_port import InquiryRepositoryPort
from app.inquiry.application.port.inquiry_reply_repository_port import InquiryReplyRepositoryPort


class CreateInquiryReplyUseCase:
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
        content: str,
        is_admin_reply: bool = False
    ) -> InquiryReply:
        inquiry = self.inquiry_repo.find_by_id(inquiry_id)
        if not inquiry:
            raise InquiryNotFoundException(inquiry_id)

        reply = InquiryReply(
            inquiry_id=inquiry_id,
            account_id=account_id,
            content=content,
            is_admin_reply=is_admin_reply,
        )

        return self.reply_repo.save(reply)