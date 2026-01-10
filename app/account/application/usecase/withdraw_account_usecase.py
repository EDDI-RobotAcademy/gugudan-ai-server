"""Withdraw account usecase - Handles account withdrawal with full data deletion."""

import json
from sqlalchemy.orm import Session as DBSession

from app.account.application.usecase.account_usecase import AccountUseCase
from app.account.infrastructure.repository.account_repository_impl import AccountRepositoryImpl
from app.common.domain.exceptions import AccountNotFoundException
from app.conversation.infrastructure.orm.chat_room_orm import ChatRoomOrm
from app.conversation.infrastructure.orm.chat_message_orm import ChatMessageOrm
from app.conversation.infrastructure.orm.chat_message_feedback_orm import ChatFeedbackOrm
from app.simulation.infrastructure.orm.simulation_chat_orm import SimulationChatORM
from app.survey.infrastructure.orm.survey_response_orm import SurveyResponseOrm
from app.inquiry.infrastructure.orm.inquiry_model import InquiryModel
from app.auth.application.usecase.session_usecase import SessionUseCase
from app.auth.infrastructure.cache.session_repository_impl import SessionRepositoryImpl


class WithdrawAccountUseCase:
    """UseCase for account withdrawal with complete data deletion.

    This usecase handles the complete deletion of all user-related data
    including chat rooms, messages, feedback, simulations, surveys, inquiries, and sessions.
    """

    def __init__(
        self,
        account_usecase: AccountUseCase,
        session_usecase: SessionUseCase,
        db_session: DBSession,
    ):
        """Initialize withdraw account usecase.

        Args:
            account_usecase: Account usecase for account operations.
            session_usecase: Session usecase for session management.
            db_session: Database session for direct data deletion.
        """
        self._account_usecase = account_usecase
        self._session_usecase = session_usecase
        self._db = db_session

    def execute(self, account_id: int) -> bool:
        """Withdraw an account and delete all associated data.

        This method deletes all user-related data in the following order:
        1. Chat feedback (must delete before chat messages)
        2. Chat messages (manually delete to avoid CASCADE depth limit)
           - First, set parent_id to NULL to break self-referential cycles
           - Then delete all messages
        3. Chat rooms (after messages are deleted)
        4. Simulation chats (account_id based)
        5. Survey responses (user_id based, CASCADE will delete response items)
        6. Inquiries (account_id based, CASCADE will delete replies)
        7. All sessions (Redis sessions by account_id)
        8. Account itself

        Args:
            account_id: The account's unique identifier.

        Returns:
            True if account was successfully withdrawn, False if account not found.

        Raises:
            AccountNotFoundException: If account doesn't exist.
        """
        # Verify account exists
        account = self._account_usecase.get_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id)

        try:
            # 1. Get all room_ids for this account first
            room_ids = [
                room.room_id 
                for room in self._db.query(ChatRoomOrm)
                .filter(ChatRoomOrm.account_id == account_id)
                .all()
            ]

            # 2. Delete chat feedback for messages in these rooms
            #    This must be deleted before chat messages to avoid FK constraint issues
            if room_ids:
                # Get message IDs for messages in the account's rooms
                message_ids = [
                    msg.id 
                    for msg in self._db.query(ChatMessageOrm)
                    .filter(ChatMessageOrm.room_id.in_(room_ids))
                    .all()
                ]
                
                # Delete feedback for those messages
                if message_ids:
                    self._db.query(ChatFeedbackOrm).filter(
                        ChatFeedbackOrm.message_id.in_(message_ids)
                    ).delete(synchronize_session=False)
            
            # Also delete feedback created by this account (if any)
            self._db.query(ChatFeedbackOrm).filter(
                ChatFeedbackOrm.account_id == account_id
            ).delete(synchronize_session=False)

            # 3. Break self-referential cycles in chat messages by setting parent_id to NULL
            #    This prevents CASCADE depth limit issues with MySQL's max depth of 15
            if room_ids:
                self._db.query(ChatMessageOrm).filter(
                    ChatMessageOrm.room_id.in_(room_ids)
                ).update({ChatMessageOrm.parent_id: None}, synchronize_session=False)

            # 4. Delete all chat messages for this account's rooms
            if room_ids:
                self._db.query(ChatMessageOrm).filter(
                    ChatMessageOrm.room_id.in_(room_ids)
                ).delete(synchronize_session=False)

            # 5. Delete chat rooms (messages are already deleted)
            self._db.query(ChatRoomOrm).filter(
                ChatRoomOrm.account_id == account_id
            ).delete(synchronize_session=False)

            # 6. Delete simulation chats
            self._db.query(SimulationChatORM).filter(
                SimulationChatORM.account_id == account_id
            ).delete(synchronize_session=False)

            # 7. Delete survey responses (CASCADE will delete response items)
            self._db.query(SurveyResponseOrm).filter(
                SurveyResponseOrm.user_id == account_id
            ).delete(synchronize_session=False)

            # 8. Delete inquiries (CASCADE will delete inquiry replies)
            # Note: Foreign key has CASCADE, but we delete explicitly for clarity
            self._db.query(InquiryModel).filter(
                InquiryModel.account_id == account_id
            ).delete(synchronize_session=False)

            # 9. Delete all sessions from Redis
            session_repo = SessionRepositoryImpl()
            session_repo.delete_all_by_account_id(account_id)

            # 10. Delete the account itself
            success = self._account_usecase.withdraw_account(account_id)

            # Commit all changes
            self._db.commit()
            return success

        except Exception as e:
            # Rollback on any error
            self._db.rollback()
            raise e
