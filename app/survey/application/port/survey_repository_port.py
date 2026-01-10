from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class SurveyRepositoryPort(ABC):
    """Survey repository port interface."""

    @abstractmethod
    def get_active_template_version(self) -> Optional[int]:
        """Get active template version number."""
        pass

    @abstractmethod
    def get_active_template_payload(self) -> Optional[dict]:
        """Get active template payload with questions.
        
        Returns:
            dict with keys: version, title, subtitle, footer, questions
            or None if no active template
        """
        pass

    @abstractmethod
    def has_user_responded(self, user_id: int, template_version: int) -> bool:
        """Check if user has already responded to a template version."""
        pass

    @abstractmethod
    def get_user_message_count(self, user_id: int) -> int:
        """Get user's message count for survey trigger condition."""
        pass

    @abstractmethod
    def save_survey_response(
        self,
        user_id: Optional[int],
        template_version: int,
        answers: dict[str, str],
    ) -> tuple[bool, bool, Optional[str]]:
        """Save survey response.
        
        Returns:
            tuple of (ok, duplicated, message)
        """
        pass
