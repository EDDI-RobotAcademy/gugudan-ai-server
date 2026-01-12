from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database.session import get_db_session
from app.survey.infrastructure.repository.survey_repository_impl import SurveyRepositoryImpl
from app.survey.adapter.input.web.request.create_survey_request import CreateSurveyRequest
from app.survey.adapter.input.web.response.survey_response import SurveyStatusResponse
from app.survey.application.usecase.get_survey_questions_usecase import GetSurveyQuestionsUseCase
from app.survey.application.usecase.get_survey_status_usecase import GetSurveyStatusUseCase
from app.survey.application.usecase.create_survey_response_usecase import CreateSurveyResponseUseCase

# ✅ 이미 가지고 있는 인증 의존성 사용
from app.account.adapter.input.web.account_router import get_current_account_id

router = APIRouter(tags=["survey"])


@router.get("/questions")
def get_questions(
    db: Session = Depends(get_db_session),
    account_id: int = Depends(get_current_account_id),
):
    """설문 표시 여부 및 설문 데이터 반환"""
    survey_repo = SurveyRepositoryImpl(db)
    usecase = GetSurveyQuestionsUseCase(survey_repo)
    
    return usecase.execute(user_id=account_id)


@router.get("/status", response_model=SurveyStatusResponse)
def get_survey_status(
    db: Session = Depends(get_db_session),
    account_id: int = Depends(get_current_account_id),
):
    """설문 완료 여부 확인 (화면에서 활성화/비활성화용)"""
    survey_repo = SurveyRepositoryImpl(db)
    usecase = GetSurveyStatusUseCase(survey_repo)
    
    result = usecase.execute(user_id=account_id)
    return SurveyStatusResponse(
        completed=result["completed"],
        template_version=result["template_version"],
    )


@router.post("/responses")
def create_response(
    req: CreateSurveyRequest,
    db: Session = Depends(get_db_session),
    account_id: int = Depends(get_current_account_id),
):
    """설문 응답 저장"""
    survey_repo = SurveyRepositoryImpl(db)
    usecase = CreateSurveyResponseUseCase(survey_repo)
    
    return usecase.execute(
        user_id=account_id,
        answers=req.answers,
    )