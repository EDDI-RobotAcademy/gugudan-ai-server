from app.conversation.domain.chat_feedback.entity import ChatFeedback


class ChatFeedbackUsecase:

    def __init__(self, chat_feedback_repo):
        self.chat_feedback_repo = chat_feedback_repo

    async def create_chat_feedback(self, chat_feedback: ChatFeedback) -> str:
        return await self.chat_feedback_repo.add_feedback(chat_feedback)

    async def update_chat_feedback(self, chat_feedback: ChatFeedback) -> str:
        return await self.chat_feedback_repo.update_feedback(chat_feedback)
