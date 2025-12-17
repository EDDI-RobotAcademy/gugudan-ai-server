"""Auth API dependencies - FastAPI dependency injection."""

from typing import Generator

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session as DBSession

from app.application.account.service import AccountService
from app.application.auth.csrf_service import CSRFService
from app.application.auth.service import AuthService
from app.application.auth.session_service import SessionService
from app.domain.auth.session import Session
from app.infrastructure.cache.session_repository import SessionRepositoryImpl
from app.infrastructure.persistence.account_repository import AccountRepositoryImpl
from config.database.session import SessionLocal


def get_db() -> Generator[DBSession, None, None]:
    """Get database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session_repository() -> SessionRepositoryImpl:
    """Get session repository dependency."""
    return SessionRepositoryImpl()


def get_account_repository(
    db: DBSession = Depends(get_db),
) -> AccountRepositoryImpl:
    """Get account repository dependency."""
    return AccountRepositoryImpl(db)


def get_csrf_service() -> CSRFService:
    """Get CSRF service dependency."""
    return CSRFService()


def get_session_service(
    session_repo: SessionRepositoryImpl = Depends(get_session_repository),
) -> SessionService:
    """Get session service dependency."""
    return SessionService(session_repo)


def get_account_service(
    account_repo: AccountRepositoryImpl = Depends(get_account_repository),
) -> AccountService:
    """Get account service dependency."""
    return AccountService(account_repo)


def get_auth_service(
    session_service: SessionService = Depends(get_session_service),
    csrf_service: CSRFService = Depends(get_csrf_service),
    account_service: AccountService = Depends(get_account_service),
) -> AuthService:
    """Get auth service dependency."""
    return AuthService(session_service, csrf_service, account_service)


def get_current_session(
    request: Request,
    session_service: SessionService = Depends(get_session_service),
) -> Session:
    """Get current session from cookie.

    Validates the session and returns it if valid.

    Raises:
        HTTPException: 401 if not authenticated or session invalid.
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    session = session_service.validate_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )

    return session


def get_optional_session(
    request: Request,
    session_service: SessionService = Depends(get_session_service),
) -> Session | None:
    """Get current session if available, None otherwise.

    Unlike get_current_session, this doesn't raise an error if not authenticated.
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        return None

    return session_service.validate_session(session_id)


def verify_csrf(
    request: Request,
    csrf_service: CSRFService = Depends(get_csrf_service),
) -> bool:
    """Verify CSRF token using Double Submit Cookie pattern.

    Raises:
        HTTPException: 403 if CSRF validation fails.
    """
    cookie_token = request.cookies.get("csrf_token")
    header_token = request.headers.get("X-CSRF-Token")

    if not csrf_service.validate_token(cookie_token, header_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token validation failed",
        )

    return True
