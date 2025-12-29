from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.adapter.input.web.dependencies import verify_admin_role
from app.config.database.session import get_db_session

from app.faq.adapter.input.web.request.create_faq_request import (
    CreateFAQRequest,
    UpdateFAQRequest,
)
from app.faq.adapter.input.web.response.faq_response import FAQResponse
from app.faq.domain.entity.faq_enums import FAQCategory
from app.faq.domain.exception import FAQNotFoundException
from app.faq.application.usecase.get_public_faqs_usecase import GetPublicFAQsUseCase
from app.faq.application.usecase.search_faqs_usecase import SearchFAQsUseCase
from app.faq.application.usecase.get_faq_detail_usecase import GetFAQDetailUseCase
from app.faq.application.usecase.create_faq_usecase import CreateFAQUseCase
from app.faq.application.usecase.update_faq_usecase import UpdateFAQUseCase
from app.faq.application.usecase.delete_faq_usecase import DeleteFAQUseCase
from app.faq.infrastructure.repository.faq_repository_impl import FAQRepositoryImpl


router = APIRouter(prefix="/faqs", tags=["faq"])


# ===========================================
# 공개 API (인증 불필요)
# ===========================================

@router.get("", response_model=List[FAQResponse])
def get_public_faqs(
    category: Optional[FAQCategory] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_session),
):
    """공개 FAQ 목록 조회 (카테고리 필터 가능)"""
    faq_repo = FAQRepositoryImpl(db)
    usecase = GetPublicFAQsUseCase(faq_repo)

    faqs = usecase.execute(
        category=category,
        offset=offset,
        limit=limit,
    )

    return [
        FAQResponse(
            id=faq.id,
            category=faq.category,
            question=faq.question,
            answer=faq.answer,
            display_order=faq.display_order,
            is_published=faq.is_published,
            view_count=faq.view_count,
            created_by=faq.created_by,
            created_at=faq.created_at,
            updated_at=faq.updated_at,
        )
        for faq in faqs
    ]


@router.get("/search", response_model=List[FAQResponse])
def search_faqs(
    keyword: str = Query(..., min_length=1),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db_session),
):
    """FAQ 검색 (FULLTEXT)"""
    faq_repo = FAQRepositoryImpl(db)
    usecase = SearchFAQsUseCase(faq_repo)

    faqs = usecase.execute(
        keyword=keyword,
        offset=offset,
        limit=limit,
    )

    return [
        FAQResponse(
            id=faq.id,
            category=faq.category,
            question=faq.question,
            answer=faq.answer,
            display_order=faq.display_order,
            is_published=faq.is_published,
            view_count=faq.view_count,
            created_by=faq.created_by,
            created_at=faq.created_at,
            updated_at=faq.updated_at,
        )
        for faq in faqs
    ]


@router.get("/{faq_id}", response_model=FAQResponse)
def get_faq_detail(
    faq_id: int,
    db: Session = Depends(get_db_session),
):
    """FAQ 상세 조회 (조회수 증가)"""
    faq_repo = FAQRepositoryImpl(db)
    usecase = GetFAQDetailUseCase(faq_repo)

    try:
        faq = usecase.execute(faq_id=faq_id, increment_view=True)
    except FAQNotFoundException:
        raise HTTPException(status_code=404, detail="FAQ를 찾을 수 없습니다")

    return FAQResponse(
        id=faq.id,
        category=faq.category,
        question=faq.question,
        answer=faq.answer,
        display_order=faq.display_order,
        is_published=faq.is_published,
        view_count=faq.view_count,
        created_by=faq.created_by,
        created_at=faq.created_at,
        updated_at=faq.updated_at,
    )


# ===========================================
# 관리자 API
# ===========================================

@router.post("", response_model=FAQResponse, status_code=201)
def create_faq(
    request: CreateFAQRequest,
    admin_id: int = Depends(verify_admin_role),
    db: Session = Depends(get_db_session),
):
    """FAQ 생성 (관리자)"""
    faq_repo = FAQRepositoryImpl(db)
    usecase = CreateFAQUseCase(faq_repo)

    faq = usecase.execute(
        category=FAQCategory(request.category),
        question=request.question,
        answer=request.answer,
        created_by=admin_id,
        display_order=request.display_order,
        is_published=request.is_published,
    )

    return FAQResponse(
        id=faq.id,
        category=faq.category,
        question=faq.question,
        answer=faq.answer,
        display_order=faq.display_order,
        is_published=faq.is_published,
        view_count=faq.view_count,
        created_by=faq.created_by,
        created_at=faq.created_at,
        updated_at=faq.updated_at,
    )


@router.put("/{faq_id}", response_model=FAQResponse)
def update_faq(
    faq_id: int,
    request: UpdateFAQRequest,
    admin_id: int = Depends(verify_admin_role),
    db: Session = Depends(get_db_session),
):
    """FAQ 수정 (관리자)"""
    faq_repo = FAQRepositoryImpl(db)
    usecase = UpdateFAQUseCase(faq_repo)

    try:
        faq = usecase.execute(
            faq_id=faq_id,
            category=FAQCategory(request.category) if request.category else None,
            question=request.question,
            answer=request.answer,
            display_order=request.display_order,
            is_published=request.is_published,
        )
    except FAQNotFoundException:
        raise HTTPException(status_code=404, detail="FAQ를 찾을 수 없습니다")

    return FAQResponse(
        id=faq.id,
        category=faq.category,
        question=faq.question,
        answer=faq.answer,
        display_order=faq.display_order,
        is_published=faq.is_published,
        view_count=faq.view_count,
        created_by=faq.created_by,
        created_at=faq.created_at,
        updated_at=faq.updated_at,
    )


@router.delete("/{faq_id}", status_code=204)
def delete_faq(
    faq_id: int,
    admin_id: int = Depends(verify_admin_role),
    db: Session = Depends(get_db_session),
):
    """FAQ 삭제 (관리자)"""
    faq_repo = FAQRepositoryImpl(db)
    usecase = DeleteFAQUseCase(faq_repo)

    try:
        usecase.execute(faq_id=faq_id)
    except FAQNotFoundException:
        raise HTTPException(status_code=404, detail="FAQ를 찾을 수 없습니다")

    return None