class InquiryNotFoundException(Exception):
    """문의를 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, inquiry_id: int):
        self.inquiry_id = inquiry_id
        super().__init__(f"Inquiry with id {inquiry_id} not found")


class InquiryAccessDeniedException(Exception):
    """문의 접근 권한이 없을 때 발생하는 예외"""
    def __init__(self, account_id: int, inquiry_id: int):
        self.account_id = account_id
        self.inquiry_id = inquiry_id
        super().__init__(f"Account {account_id} has no access to inquiry {inquiry_id}")


class InquiryReplyNotFoundException(Exception):
    """답변을 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, reply_id: int):
        self.reply_id = reply_id
        super().__init__(f"InquiryReply with id {reply_id} not found")