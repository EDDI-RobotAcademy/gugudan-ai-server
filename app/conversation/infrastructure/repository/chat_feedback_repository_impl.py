from sqlalchemy.orm import Session

from app.conversation.domain.chat_feedback.entity import ChatFeedback
from app.conversation.infrastructure.orm.chat_message_feedback_orm import MessageFeedbackModel
from app.conversation.infrastructure.orm.chat_message_orm import ChatMessageOrm


class ChatFeedbackRepositoryImpl:
    def __init__(self, session: Session):
        self.db = session

    async def add_feedback(self, feedback: ChatFeedback):

        try:
            if feedback.id is None:
                # 1. 대상 message 정보 확인
                exists = (self.db.query(ChatMessageOrm)
                          .filter(
                    ChatMessageOrm.id == feedback.message_id,

                ).first())

                # 신규 행 insert
                if exists:
                    msg = MessageFeedbackModel(
                        message_id=feedback.message_id,
                        account_id=feedback.account_id,
                        satisfaction=feedback.satisfaction,
                        emotion_label=feedback.emotion_label,
                        emotion_score=feedback.emotion_score,
                        feedback_text=feedback.feedback_text
                    )

                    self.db.add(msg)
                    self.db.commit()
                    self.db.refresh(msg)

            else:
                await self.update_feedback(feedback)

        except Exception as e:
            self.db.rollback()
            raise e

        finally:
            self.db.close()

        return f"success"

    async def update_feedback(self, feedback: ChatFeedback):

        if feedback.id is None:
            return None

        try:
            exists = (self.db.query(MessageFeedbackModel)
                      .filter(
                MessageFeedbackModel.id == feedback.id
            ).first())

            if not exists:
                return None

            exists.message_id = feedback.message_id
            exists.account_id = feedback.account_id
            exists.satisfaction = feedback.satisfaction
            exists.emotion_label = feedback.emotion_label
            exists.emotion_score = feedback.emotion_score
            exists.feedback_text = feedback.feedback_text

            self.db.commit()
            self.db.refresh(exists)

        except Exception as e:
            self.db.rollback()
            raise e

        finally:
            self.db.close()

        return f"success"