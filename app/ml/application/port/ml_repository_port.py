from abc import ABC, abstractmethod
from typing import Optional

from app.ml.infrastructure.orm.chat_message_analysis_model import ChatMessageAnalysisModel


class MLRepositoryPort(ABC):

    @abstractmethod
    def get_counsel_data(self, chat_message_id: int, chat_message_feedback_id: int) -> Optional[dict]:
        pass


    @abstractmethod
    def make_counsel_data_to_analysis(self, message_id: int, feedback_id: int) -> Optional[ChatMessageAnalysisModel]:
        pass

