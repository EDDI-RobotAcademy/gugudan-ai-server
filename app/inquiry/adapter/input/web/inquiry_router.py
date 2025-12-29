from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.adapter.input.web.dependencies import (
    get_current_jwt_payload,
    verify_admin_role,
)
from app.auth.application.port.jwt_token_port import TokenPayload
from app.config.database.session import get_db_session

from app.inquiry.adapter.input.web.request.create_inquiry_request import CreateInquiryRequest
from app.inquiry.adapter.input.web.request.create_reply_request import CreateReplyRequest
from app.inquiry.adapter.input.web.request.update_status_request import UpdateStatusRequest
from app.inquiry.adapter.input.web.response.inquiry_response import (
    InquiryResponse,
    InquiryDetailResponse,
    InquiryReplyResponse,
)
from app.inquiry.domain.entity.inquiry_enums import InquiryStatus, InquiryCategory
from app.inquiry.domain.exception import (
    InquiryNotFoundException,
    InquiryAccessDeniedException,
)
from app.inquiry.application.usecase.create_inquiry_usecase import CreateInquiryUseCase
from app.inquiry.application.usecase.get_my_inquiries_usecase import GetMyInquiriesUseCase
from app.inquiry.application.usecase.get_inquiry_detail_usecase import GetInquiryDetailUseCase
from app.inquiry.application.usecase.get_all_inquiries_usecase import GetAllInquiriesUseCase
from app.inquiry.application.usecase.create_inquiry_reply_usecase import CreateInquiryReplyUseCase
from app.inquiry.application.usecase.update_inquiry_status_usecase import UpdateInquiryStatusUseCase
from app.inquiry.infrastructure.repository.inquiry_repository_impl import InquiryRepositoryImpl
from app.inquiry.infrastructure.repository.inquiry_reply_repository_impl import InquiryReplyRepositoryImpl


router = APIRouter(prefix="/inquiries", tags=["inquiry"])


# ===========================================
# 사용자 API
# ===========================================

@router.post("", response_model=InquiryResponse, status_code=201)
def create_inquiry(
    request: CreateInquiryRequest,
    jwt_payload: TokenPayload = Depends(get_current_jwt_payload),
    db: Session = Depends(get_db_session),
):
    """문의 생성"""
    inquiry_repo = InquiryRepositoryImpl(db)
    usecase = CreateInquiryUseCase(inquiry_repo)

    inquiry = usecase.execute(
        account_id=jwt_payload.account_id,
        category=InquiryCategory(request.category),
        title=request.title,
        content=request.content,
    )

    return InquiryResponse(
        id=inquiry.id,
        account_id=inquiry.account_id,
        category=inquiry.category,
        title=inquiry.title,
        content=inquiry.content,
        status=inquiry.status,
        created_at=inquiry.created_at,
        updated_at=inquiry.updated_at,
    )


@router.get("/my", response_model=List[InquiryResponse])
def get_my_inquiries(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    jwt_payload: TokenPayload = Depends(get_current_jwt_payload),
    db: Session = Depends(get_db_session),
):
    """내 문의 목록 조회"""
    inquiry_repo = InquiryRepositoryImpl(db)
    usecase = GetMyInquiriesUseCase(inquiry_repo)

    inquiries = usecase.execute(
        account_id=jwt_payload.account_id,
        offset=offset,
        limit=limit,
    )

    return [
        InquiryResponse(
            id=inquiry.id,
            account_id=inquiry.account_id,
            category=inquiry.category,
            title=inquiry.title,
            content=inquiry.content,
            status=inquiry.status,
            created_at=inquiry.created_at,
            updated_at=inquiry.updated_at,
        )
        for inquiry in inquiries
    ]


@router.get("/{inquiry_id}", response_model=InquiryDetailResponse)
def get_inquiry_detail(
    inquiry_id: int,
    jwt_payload: TokenPayload = Depends(get_current_jwt_payload),
    db: Session = Depends(get_db_session),
):
    """문의 상세 조회 (답변 포함)"""
    inquiry_repo = InquiryRepositoryImpl(db)
    reply_repo = InquiryReplyRepositoryImpl(db)
    usecase = GetInquiryDetailUseCase(inquiry_repo, reply_repo)

    try:
        # 관리자 여부 확인
        is_admin = hasattr(jwt_payload, 'role') and jwt_payload.role == 'ADMIN'

        result = usecase.execute(
            inquiry_id=inquiry_id,
            account_id=jwt_payload.account_id,
            is_admin=is_admin,
        )
    except InquiryNotFoundException:
        raise HTTPException(status_code=404, detail="문의를 찾을 수 없습니다")
    except InquiryAccessDeniedException:
        raise HTTPException(status_code=403, detail="접근 권한이 없습니다")

    return InquiryDetailResponse(
        inquiry=InquiryResponse(
            id=result["inquiry"].id,
            account_id=result["inquiry"].account_id,
            category=result["inquiry"].category,
            title=result["inquiry"].title,
            content=result["inquiry"].content,
            status=result["inquiry"].status,
            created_at=result["inquiry"].created_at,
            updated_at=result["inquiry"].updated_at,
        ),
        replies=[
            InquiryReplyResponse(
                id=reply.id,
                inquiry_id=reply.inquiry_id,
                account_id=reply.account_id,
                content=reply.content,
                is_admin_reply=reply.is_admin_reply,
                created_at=reply.created_at,
            )
            for reply in result["replies"]
        ],
    )


# ===========================================
# 관리자 API
# ===========================================

@router.get("/admin/all", response_model=List[InquiryResponse])
def get_all_inquiries(
    status: Optional[InquiryStatus] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    admin_id: int = Depends(verify_admin_role),
    db: Session = Depends(get_db_session),
):
    """전체 문의 목록 조회 (관리자)"""
    inquiry_repo = InquiryRepositoryImpl(db)
    usecase = GetAllInquiriesUseCase(inquiry_repo)

    inquiries = usecase.execute(
        status=status,
        offset=offset,
        limit=limit,
    )

    return [
        InquiryResponse(
            id=inquiry.id,
            account_id=inquiry.account_id,
            category=inquiry.category,
            title=inquiry.title,
            content=inquiry.content,
            status=inquiry.status,
            created_at=inquiry.created_at,
            updated_at=inquiry.updated_at,
        )
        for inquiry in inquiries
    ]


@router.post("/{inquiry_id}/replies", response_model=InquiryReplyResponse, status_code=201)
def create_inquiry_reply(
    inquiry_id: int,
    request: CreateReplyRequest,
    jwt_payload: TokenPayload = Depends(get_current_jwt_payload),
    db: Session = Depends(get_db_session),
):
    """문의에 답변 작성 (사용자 본인 또는 관리자)"""
    inquiry_repo = InquiryRepositoryImpl(db)
    reply_repo = InquiryReplyRepositoryImpl(db)
    usecase = CreateInquiryReplyUseCase(inquiry_repo, reply_repo)

    try:
        # 문의 조회
        inquiry = inquiry_repo.find_by_id(inquiry_id)
        if not inquiry:
            raise InquiryNotFoundException()

        # 권한 확인: 관리자가 아니면 본인의 문의에만 답변 가능
        is_admin = hasattr(jwt_payload, 'role') and jwt_payload.role == 'ADMIN'
        if not is_admin and inquiry.account_id != jwt_payload.account_id:
            raise InquiryAccessDeniedException()

        reply = usecase.execute(
            inquiry_id=inquiry_id,
            account_id=jwt_payload.account_id,
            content=request.content,
            is_admin_reply=is_admin,
        )
    except InquiryNotFoundException:
        raise HTTPException(status_code=404, detail="문의를 찾을 수 없습니다")
    except InquiryAccessDeniedException:
        raise HTTPException(status_code=403, detail="본인의 문의에만 답변할 수 있습니다")

    return InquiryReplyResponse(
        id=reply.id,
        inquiry_id=reply.inquiry_id,
        account_id=reply.account_id,
        content=reply.content,
        is_admin_reply=reply.is_admin_reply,
        created_at=reply.created_at,
    )


@router.patch("/{inquiry_id}/status", response_model=InquiryResponse)
def update_inquiry_status(
    inquiry_id: int,
    request: UpdateStatusRequest,
    admin_id: int = Depends(verify_admin_role),
    db: Session = Depends(get_db_session),
):
    """문의 상태 변경 (관리자)"""
    inquiry_repo = InquiryRepositoryImpl(db)
    usecase = UpdateInquiryStatusUseCase(inquiry_repo)

    try:
        inquiry = usecase.execute(
            inquiry_id=inquiry_id,
            new_status=InquiryStatus(request.status),
        )
    except InquiryNotFoundException:
        raise HTTPException(status_code=404, detail="문의를 찾을 수 없습니다")

    return InquiryResponse(
        id=inquiry.id,
        account_id=inquiry.account_id,
        category=inquiry.category,
        title=inquiry.title,
        content=inquiry.content,
        status=inquiry.status,
        created_at=inquiry.created_at,
        updated_at=inquiry.updated_at,
    )