from datetime import datetime
from typing import Optional


class InquiryReply:
    def __init__(
        self,
        inquiry_id: int,
        account_id: int,
        content: str,
        is_admin_reply: bool = False,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.inquiry_id = inquiry_id
        self.account_id = account_id
        self.content = content
        self.is_admin_reply = is_admin_reply
        self.created_at = created_at or datetime.utcnow()