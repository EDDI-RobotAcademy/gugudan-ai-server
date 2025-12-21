from pydantic import BaseModel, Field
from datetime import datetime

from app.conversation.domain.chat_feedback.enums import SatisfiedStatus


class ChatFeedback(BaseModel):
    id: int | None = None
    message_id: int
    account_id: int
    satisfaction: SatisfiedStatus
    emotion_label: int | None = None
    emotion_score: float | None = None
    feedback_text: int | None = None
    created_at: datetime | None = None