from datetime import datetime
from typing import Optional
from app.inquiry.domain.entity.inquiry_enums import InquiryStatus, InquiryCategory


class Inquiry:
    def __init__(
        self,
        account_id: int,
        category: InquiryCategory,
        title: str,
        content: str,
        id: Optional[int] = None,
        status: InquiryStatus = InquiryStatus.PENDING,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.account_id = account_id
        self.category = category
        self.title = title
        self.content = content
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def is_owned_by(self, account_id: int) -> bool:
        """해당 계정이 문의 작성자인지 확인"""
        return self.account_id == account_id

    def start_progress(self) -> None:
        """문의 처리 시작"""
        if self.status != InquiryStatus.PENDING:
            raise ValueError(f"Cannot start progress from status: {self.status}")
        self.status = InquiryStatus.IN_PROGRESS
        self.updated_at = datetime.utcnow()

    def resolve(self) -> None:
        """문의 해결"""
        if self.status not in [InquiryStatus.PENDING, InquiryStatus.IN_PROGRESS]:
            raise ValueError(f"Cannot resolve from status: {self.status}")
        self.status = InquiryStatus.RESOLVED
        self.updated_at = datetime.utcnow()

    def close(self) -> None:
        """문의 종료"""
        if self.status != InquiryStatus.RESOLVED:
            raise ValueError(f"Cannot close from status: {self.status}")
        self.status = InquiryStatus.CLOSED
        self.updated_at = datetime.utcnow()

    def update_status(self, new_status: InquiryStatus) -> None:
        """상태 직접 변경 (관리자용)"""
        self.status = new_status
        self.updated_at = datetime.utcnow()