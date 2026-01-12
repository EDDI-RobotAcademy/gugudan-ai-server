from __future__ import annotations
import os
from app.survey.application.port.survey_repository_port import SurveyRepositoryPort


class GetSurveyQuestionsUseCase:
    """UseCase for getting survey questions with display conditions."""

    def __init__(self, survey_repo: SurveyRepositoryPort):
        self._survey_repo = survey_repo
        self._trigger_message_count = int(os.getenv("SURVEY_TRIGGER_MESSAGE_COUNT", "5"))

    def execute(self, user_id: int) -> dict:
        """Get survey questions if conditions are met.
        
        Args:
            user_id: User account ID
            
        Returns:
            dict with show flag and survey data or reason for not showing
        """
        # 1) 활성 템플릿 조회
        payload = self._survey_repo.get_active_template_payload()
        if not payload:
            return {"show": False, "reason": "no_active_template"}

        if not payload.get("questions"):
            return {"show": False, "reason": "invalid_payload"}

        template_version = payload.get("version")

        # 2) 이미 응답했으면 show=false
        if self._survey_repo.has_user_responded(user_id=user_id, template_version=template_version):
            return {"show": False, "reason": "already_responded"}

        # 3) 메시지 카운트 조건
        msg_count = self._survey_repo.get_user_message_count(user_id=user_id)
        if msg_count < self._trigger_message_count:
            return {
                "show": False,
                "reason": "not_enough_messages",
                "trigger": self._trigger_message_count,
                "current": msg_count,
            }

        # 4) 보여준다
        return {
            "show": True,
            "title": payload.get("title"),
            "subtitle": payload.get("subtitle"),
            "footer": payload.get("footer"),
            "version": template_version,
            "questions": payload.get("questions"),
        }
