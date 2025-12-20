from abc import ABC, abstractmethod
from typing import List

from app.conversation.infrastructure.orm.chat_message_orm import ChatMessageOrm


class MLRepositoryPort(ABC):

    @abstractmethod
    def get_counsel_data(self, start: str, end: str) -> List[ChatMessageOrm]:
        pass
