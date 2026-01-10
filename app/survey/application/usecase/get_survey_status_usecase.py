from __future__ import annotations
from app.survey.application.port.survey_repository_port import SurveyRepositoryPort


class GetSurveyStatusUseCase:
    """UseCase for checking survey completion status."""

    def __init__(self, survey_repo: SurveyRepositoryPort):
        self._survey_repo = survey_repo

    def execute(self, user_id: int) -> dict:
        """Get survey completion status.
        
        Args:
            user_id: User account ID
            
        Returns:
            dict with completed flag and template_version
        """
        template_version = self._survey_repo.get_active_template_version()
        
        if template_version is None:
            return {
                "completed": False,
                "template_version": None,
            }
        
        completed = self._survey_repo.has_user_responded(
            user_id=user_id,
            template_version=template_version
        )
        
        return {
            "completed": completed,
            "template_version": template_version,
        }
