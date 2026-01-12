from __future__ import annotations
from app.survey.application.port.survey_repository_port import SurveyRepositoryPort


class CreateSurveyResponseUseCase:
    """UseCase for creating survey response."""

    def __init__(self, survey_repo: SurveyRepositoryPort):
        self._survey_repo = survey_repo

    def execute(
        self,
        user_id: int,
        answers: dict[str, str],
    ) -> dict:
        """Create survey response.
        
        Args:
            user_id: User account ID
            answers: Dictionary of question_id -> answer value
            
        Returns:
            dict with ok, duplicated, and message fields
        """
        template_version = self._survey_repo.get_active_template_version()
        
        if template_version is None:
            return {
                "ok": False,
                "duplicated": False,
                "message": "설문 템플릿이 없습니다.",
            }

        ok, duplicated, message = self._survey_repo.save_survey_response(
            user_id=user_id,
            template_version=template_version,
            answers=answers,
        )
        
        return {
            "ok": ok,
            "duplicated": duplicated,
            "message": message,
        }
