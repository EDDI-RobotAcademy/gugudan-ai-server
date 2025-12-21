from datetime import datetime
from .enums import SatisfiedStatus


class ChatFeedback:

    def __init__(
            self,
            id: int | None,
            message_id: int,
            account_id: int,
            satisfaction: SatisfiedStatus,
            emotion_label: int | None,
            emotion_score: float | None,
            feedback_text: int | None,
            created_at: datetime | None = None,
    ):
        self.id = id
        self.message_id = message_id
        self.account_id = account_id
        self.satisfaction = satisfaction
        self.emotion_label = emotion_label
        self.emotion_score = emotion_score
        self.feedback_text = feedback_text
        self.created_at = created_at
        self.updated_at = created_at
