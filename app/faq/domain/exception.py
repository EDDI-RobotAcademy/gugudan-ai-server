class FAQNotFoundException(Exception):
    """FAQ를 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, faq_id: int):
        self.faq_id = faq_id
        super().__init__(f"FAQ with id {faq_id} not found")