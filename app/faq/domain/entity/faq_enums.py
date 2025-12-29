from enum import Enum


class FAQCategory(str, Enum):
    GENERAL = "GENERAL"  # 일반
    ACCOUNT = "ACCOUNT"  # 계정 관련
    BILLING = "BILLING"  # 결제/환불
    TECHNICAL = "TECHNICAL"  # 기술 지원
    SERVICE = "SERVICE"  # 서비스 이용
    OTHER = "OTHER"  # 기타