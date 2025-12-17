"""Auth ports - Interfaces for authentication adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from app.domain.auth.session import Session


@dataclass
class OAuthUserInfo:
    """User information retrieved from OAuth provider."""

    email: str
    name: str
    picture: Optional[str] = None
    provider: Optional[str] = None


class SessionRepositoryPort(ABC):
    """Port (interface) for session repository.

    Sessions are stored server-side (e.g., in Redis) with TTL-based expiration.
    """

    @abstractmethod
    def save(self, session: Session) -> None:
        """Save a session.

        Args:
            session: The session to save.
        """
        pass

    @abstractmethod
    def find_by_id(self, session_id: str) -> Optional[Session]:
        """Find a session by its ID.

        Args:
            session_id: The session's unique identifier.

        Returns:
            The Session if found and not expired, None otherwise.
        """
        pass

    @abstractmethod
    def delete(self, session_id: str) -> None:
        """Delete a session.

        Args:
            session_id: The session's unique identifier.
        """
        pass

    @abstractmethod
    def extend_ttl(self, session_id: str, ttl_seconds: int) -> bool:
        """Extend the TTL of a session.

        Args:
            session_id: The session's unique identifier.
            ttl_seconds: New TTL in seconds.

        Returns:
            True if session was found and extended, False otherwise.
        """
        pass


class OAuthProviderPort(ABC):
    """Port (interface) for OAuth provider adapters.

    Each OAuth provider (Google, Kakao, Naver) implements this interface.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get the name of this OAuth provider."""
        pass

    @abstractmethod
    def get_authorization_url(self, state: str) -> str:
        """Get the URL to redirect user to for OAuth authorization.

        Args:
            state: CSRF state token to include in the request.

        Returns:
            The authorization URL to redirect the user to.
        """
        pass

    @abstractmethod
    async def exchange_code_for_token(self, code: str) -> str:
        """Exchange authorization code for access token.

        Args:
            code: The authorization code from OAuth callback.

        Returns:
            The access token.

        Raises:
            OAuthException: If token exchange fails.
        """
        pass

    @abstractmethod
    async def get_user_info(self, access_token: str) -> OAuthUserInfo:
        """Get user information using access token.

        Args:
            access_token: The OAuth access token.

        Returns:
            User information from the OAuth provider.

        Raises:
            OAuthException: If fetching user info fails.
        """
        pass
