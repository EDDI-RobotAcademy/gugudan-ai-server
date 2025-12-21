from abc import ABC, abstractmethod
from datetime import datetime

from app.conversation.domain.chat_feedback.enums import SatisfiedStatus


class ChatFeedbackRepositoryPort(ABC):

    @abstractmethod
    async def create_chat_feedback(
            self,
            id: int | None,
            message_id: int,
            account_id: int,
            satisfaction: SatisfiedStatus,
            emotion_label: int | None,
            emotion_score: float | None,
            feedback_text: int | None,
            created_at: datetime | None = None,

    ) -> str:
        pass

    @abstractmethod
    async def update_chat_feedback(
            self,
            id: int | None,
            message_id: int,
            account_id: int,
            satisfaction: SatisfiedStatus,
            emotion_label: int | None,
            emotion_score: float | None,
            feedback_text: int | None,
            created_at: datetime | None = None,
    ) -> str:
        pass