from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.auth.adapter.input.web.dependencies import (
    get_optional_jwt_payload,
    get_optional_session,
)
from app.auth.application.port.jwt_token_port import TokenPayload
from app.auth.domain.entity.session import Session as AuthSession
from app.auth.application.usecase.session_usecase import SessionUseCase
from app.auth.infrastructure.cache.session_repository_impl import SessionRepositoryImpl
from app.config.database.session import get_db_session

from app.account.adapter.input.web.response.update_mbti_gender_response import UpdateMbtiGenderResponse
from app.account.adapter.input.web.request.update_mbti_gender_Request import UpdateMbtiGenderRequest
from app.account.adapter.input.web.response.withdraw_account_response import WithdrawAccountResponse

from app.account.adapter.input.web.response.update_mbti_gender_response import (
    UpdateMbtiGenderResponse,
)
from app.account.application.usecase.account_usecase import AccountUseCase
from app.account.application.usecase.withdraw_account_usecase import WithdrawAccountUseCase
from app.account.infrastructure.repository.account_repository_impl import AccountRepositoryImpl
from app.common.domain.exceptions import AccountNotFoundException


# =============================
# DI 객체 (conversation_router 스타일)
# =============================
account_repo = AccountRepositoryImpl()
account_usecase = AccountUseCase(account_repo)

router = APIRouter(prefix="/account", tags=["account"])


# =============================
# 인증 관련
# =============================
def get_current_account_id(
    jwt_payload: TokenPayload | None = Depends(get_optional_jwt_payload),
    session: AuthSession | None = Depends(get_optional_session),
) -> int:

    if jwt_payload:
        return jwt_payload.account_id
    if session:
        return session.account_id
    raise HTTPException(status_code=401, detail="Not authenticated")


# =============================
# PATCH 내 MBTI / Gender 수정
# =============================
@router.patch("/my/profile/mbti-gender/edit", response_model=UpdateMbtiGenderResponse)
def edit_my_mbti_gender(
    req: UpdateMbtiGenderRequest,
    account_id: int = Depends(get_current_account_id),
    db: DBSession = Depends(get_db_session),
):
    if req.gender is None and req.mbti is None:
        raise HTTPException(status_code=400, detail="Nothing to update")

    repo = AccountRepositoryImpl(db)
    usecase = AccountUseCase(repo)

    updated = usecase.update_my_mbti_gender(
        account_id=account_id,
        gender=req.gender,
        mbti=req.mbti,
    )

    return UpdateMbtiGenderResponse(
        account_id=updated.id,
        gender=updated.gender,
        mbti=updated.mbti,
    )


# =============================
# DELETE 회원 탈퇴
# =============================
@router.delete("/withdraw", response_model=WithdrawAccountResponse)
def withdraw_my_account(
    account_id: int = Depends(get_current_account_id),
    db: DBSession = Depends(get_db_session),
):
    """회원 탈퇴 - 모든 사용자 관련 데이터 삭제"""
    try:
        # Initialize dependencies
        account_repo = AccountRepositoryImpl(db)
        account_usecase = AccountUseCase(account_repo)
        session_repo = SessionRepositoryImpl()
        session_usecase = SessionUseCase(session_repo)
        
        # Create withdraw usecase
        withdraw_usecase = WithdrawAccountUseCase(
            account_usecase=account_usecase,
            session_usecase=session_usecase,
            db_session=db,
        )
        
        # Execute withdrawal
        success = withdraw_usecase.execute(account_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다.")
        
        return WithdrawAccountResponse(
            message="회원 탈퇴가 완료되었습니다. 모든 데이터가 삭제되었습니다.",
            account_id=account_id,
        )
    except AccountNotFoundException:
        raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"회원 탈퇴 중 오류가 발생했습니다: {str(e)}")

