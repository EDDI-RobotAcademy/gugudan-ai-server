from enum import Enum


class InquiryStatus(str, Enum):
    """문의 상태"""
    PENDING = "PENDING"  # 대기중
    IN_PROGRESS = "IN_PROGRESS"  # 처리중
    RESOLVED = "RESOLVED"  # 해결됨
    CLOSED = "CLOSED"  # 종료


class InquiryCategory(str, Enum):
    """문의 카테고리"""
    GENERAL = "GENERAL"  # 일반 문의
    ACCOUNT = "ACCOUNT"  # 계정 관련
    BILLING = "BILLING"  # 결제/환불
    TECHNICAL = "TECHNICAL"  # 기술 지원
    BUG_REPORT = "BUG_REPORT"  # 버그 신고
    FEATURE_REQUEST = "FEATURE_REQUEST"  # 기능 요청
    OTHER = "OTHER"  # 기타
