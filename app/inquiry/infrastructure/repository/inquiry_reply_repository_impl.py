from typing import Optional, List
from sqlalchemy.orm import Session as DBSession
from app.config.database.session import get_db_session

from app.inquiry.domain.entity.inquiry_reply import InquiryReply
from app.inquiry.application.port.inquiry_reply_repository_port import InquiryReplyRepositoryPort
from app.inquiry.infrastructure.orm.inquiry_reply_model import InquiryReplyModel


class InquiryReplyRepositoryImpl(InquiryReplyRepositoryPort):
    def __init__(self, db_session: Optional[DBSession] = None):
        self._session: DBSession = db_session or get_db_session()

    def save(self, reply: InquiryReply) -> InquiryReply:
        try:
            if reply.id is None:
                model = self._to_model(reply)
                self._session.add(model)
                self._session.commit()
                self._session.refresh(model)
                return self._to_entity(model)
            else:
                model = (
                    self._session.query(InquiryReplyModel)
                    .filter(InquiryReplyModel.id == reply.id)
                    .first()
                )
                if model:
                    model.content = reply.content
                    self._session.commit()
                    self._session.refresh(model)
                    return self._to_entity(model)
                else:
                    model = self._to_model(reply)
                    self._session.add(model)
                    self._session.commit()
                    self._session.refresh(model)
                    return self._to_entity(model)
        finally:
            self._session.close()

    def find_by_id(self, reply_id: int) -> Optional[InquiryReply]:
        try:
            model = (
                self._session.query(InquiryReplyModel)
                .filter(InquiryReplyModel.id == reply_id)
                .first()
            )
            return self._to_entity(model) if model else None
        finally:
            self._session.close()

    def find_by_inquiry_id(self, inquiry_id: int) -> List[InquiryReply]:
        try:
            models = (
                self._session.query(InquiryReplyModel)
                .filter(InquiryReplyModel.inquiry_id == inquiry_id)
                .order_by(InquiryReplyModel.created_at.asc())
                .all()
            )
            return [self._to_entity(model) for model in models]
        finally:
            self._session.close()

    def delete(self, reply_id: int) -> bool:
        try:
            model = (
                self._session.query(InquiryReplyModel)
                .filter(InquiryReplyModel.id == reply_id)
                .first()
            )
            if model:
                self._session.delete(model)
                self._session.commit()
                return True
            return False
        finally:
            self._session.close()

    @staticmethod
    def _to_entity(model: InquiryReplyModel) -> InquiryReply:
        return InquiryReply(
            id=model.id,
            inquiry_id=model.inquiry_id,
            account_id=model.account_id,
            content=model.content,
            is_admin_reply=model.is_admin_reply,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(entity: InquiryReply) -> InquiryReplyModel:
        return InquiryReplyModel(
            id=entity.id,
            inquiry_id=entity.inquiry_id,
            account_id=entity.account_id,
            content=entity.content,
            is_admin_reply=entity.is_admin_reply,
            created_at=entity.created_at,
        )