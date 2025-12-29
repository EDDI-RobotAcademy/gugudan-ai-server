from typing import Optional, List
from sqlalchemy.orm import Session as DBSession
from app.config.database.session import get_db_session

from app.inquiry.domain.entity.inquiry import Inquiry
from app.inquiry.domain.entity.inquiry_enums import InquiryStatus, InquiryCategory
from app.inquiry.application.port.inquiry_repository_port import InquiryRepositoryPort
from app.inquiry.infrastructure.orm.inquiry_model import InquiryModel


class InquiryRepositoryImpl(InquiryRepositoryPort):
    def __init__(self, db_session: Optional[DBSession] = None):
        self._session: DBSession = db_session or get_db_session()

    def save(self, inquiry: Inquiry) -> Inquiry:
        try:
            if inquiry.id is None:
                model = self._to_model(inquiry)
                self._session.add(model)
                self._session.commit()
                self._session.refresh(model)
                return self._to_entity(model)
            else:
                model = (
                    self._session.query(InquiryModel)
                    .filter(InquiryModel.id == inquiry.id)
                    .first()
                )
                if model:
                    model.category = inquiry.category.value
                    model.title = inquiry.title
                    model.content = inquiry.content
                    model.status = inquiry.status.value
                    model.updated_at = inquiry.updated_at
                    self._session.commit()
                    self._session.refresh(model)
                    return self._to_entity(model)
                else:
                    model = self._to_model(inquiry)
                    self._session.add(model)
                    self._session.commit()
                    self._session.refresh(model)
                    return self._to_entity(model)
        finally:
            self._session.close()

    def find_by_id(self, inquiry_id: int) -> Optional[Inquiry]:
        try:
            model = (
                self._session.query(InquiryModel)
                .filter(InquiryModel.id == inquiry_id)
                .first()
            )
            return self._to_entity(model) if model else None
        finally:
            self._session.close()

    def find_by_account_id(
        self,
        account_id: int,
        offset: int = 0,
        limit: int = 20
    ) -> List[Inquiry]:
        try:
            models = (
                self._session.query(InquiryModel)
                .filter(InquiryModel.account_id == account_id)
                .order_by(InquiryModel.created_at.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self._to_entity(model) for model in models]
        finally:
            self._session.close()

    def find_all(
        self,
        status: Optional[InquiryStatus] = None,
        offset: int = 0,
        limit: int = 20
    ) -> List[Inquiry]:
        try:
            query = self._session.query(InquiryModel)

            if status:
                query = query.filter(InquiryModel.status == status.value)

            models = (
                query
                .order_by(InquiryModel.created_at.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self._to_entity(model) for model in models]
        finally:
            self._session.close()

    def delete(self, inquiry_id: int) -> bool:
        try:
            model = (
                self._session.query(InquiryModel)
                .filter(InquiryModel.id == inquiry_id)
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
    def _to_entity(model: InquiryModel) -> Inquiry:
        return Inquiry(
            id=model.id,
            account_id=model.account_id,
            category=InquiryCategory(model.category),
            title=model.title,
            content=model.content,
            status=InquiryStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(entity: Inquiry) -> InquiryModel:
        return InquiryModel(
            id=entity.id,
            account_id=entity.account_id,
            category=entity.category.value,
            title=entity.title,
            content=entity.content,
            status=entity.status.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )