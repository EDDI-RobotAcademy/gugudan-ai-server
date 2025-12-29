from typing import Optional, List
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text
from app.config.database.session import get_db_session

from app.faq.domain.entity.faq import FAQ
from app.faq.domain.entity.faq_enums import FAQCategory
from app.faq.application.port.faq_repository_port import FAQRepositoryPort
from app.faq.infrastructure.orm.faq_model import FAQModel


class FAQRepositoryImpl(FAQRepositoryPort):
    def __init__(self, db_session: Optional[DBSession] = None):
        self._session: DBSession = db_session or get_db_session()

    def save(self, faq: FAQ) -> FAQ:
        try:
            if faq.id is None:
                model = self._to_model(faq)
                self._session.add(model)
                self._session.commit()
                self._session.refresh(model)
                return self._to_entity(model)
            else:
                model = (
                    self._session.query(FAQModel)
                    .filter(FAQModel.id == faq.id)
                    .first()
                )
                if model:
                    model.category = faq.category.value
                    model.question = faq.question
                    model.answer = faq.answer
                    model.display_order = faq.display_order
                    model.is_published = faq.is_published
                    model.view_count = faq.view_count
                    model.updated_at = faq.updated_at
                    self._session.commit()
                    self._session.refresh(model)
                    return self._to_entity(model)
                else:
                    model = self._to_model(faq)
                    self._session.add(model)
                    self._session.commit()
                    self._session.refresh(model)
                    return self._to_entity(model)
        finally:
            self._session.close()

    def find_by_id(self, faq_id: int) -> Optional[FAQ]:
        try:
            model = (
                self._session.query(FAQModel)
                .filter(FAQModel.id == faq_id)
                .first()
            )
            return self._to_entity(model) if model else None
        finally:
            self._session.close()

    def find_published(
        self,
        category: Optional[FAQCategory] = None,
        offset: int = 0,
        limit: int = 20
    ) -> List[FAQ]:
        try:
            query = self._session.query(FAQModel).filter(FAQModel.is_published == True)

            if category:
                query = query.filter(FAQModel.category == category.value)

            models = (
                query
                .order_by(FAQModel.display_order.asc(), FAQModel.created_at.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self._to_entity(model) for model in models]
        finally:
            self._session.close()

    def search(
        self,
        keyword: str,
        offset: int = 0,
        limit: int = 20
    ) -> List[FAQ]:
        try:
            # Using MATCH AGAINST for fulltext search
            query = text("""
                SELECT * FROM faq
                WHERE MATCH(question, answer) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
                AND is_published = 1
                ORDER BY display_order ASC
                LIMIT :limit OFFSET :offset
            """)

            result = self._session.execute(
                query,
                {"keyword": keyword, "limit": limit, "offset": offset}
            )

            faqs = []
            for row in result:
                model = FAQModel(
                    id=row.id,
                    category=row.category,
                    question=row.question,
                    answer=row.answer,
                    display_order=row.display_order,
                    is_published=row.is_published,
                    view_count=row.view_count,
                    created_by=row.created_by,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                faqs.append(self._to_entity(model))

            return faqs
        finally:
            self._session.close()

    def find_all(
        self,
        offset: int = 0,
        limit: int = 20
    ) -> List[FAQ]:
        try:
            models = (
                self._session.query(FAQModel)
                .order_by(FAQModel.display_order.asc(), FAQModel.created_at.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self._to_entity(model) for model in models]
        finally:
            self._session.close()

    def increment_view_count(self, faq_id: int) -> bool:
        try:
            model = (
                self._session.query(FAQModel)
                .filter(FAQModel.id == faq_id)
                .first()
            )
            if model:
                model.view_count += 1
                self._session.commit()
                return True
            return False
        finally:
            self._session.close()

    def delete(self, faq_id: int) -> bool:
        try:
            model = (
                self._session.query(FAQModel)
                .filter(FAQModel.id == faq_id)
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
    def _to_entity(model: FAQModel) -> FAQ:
        return FAQ(
            id=model.id,
            category=FAQCategory(model.category),
            question=model.question,
            answer=model.answer,
            display_order=model.display_order,
            is_published=model.is_published,
            view_count=model.view_count,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(entity: FAQ) -> FAQModel:
        return FAQModel(
            id=entity.id,
            category=entity.category.value,
            question=entity.question,
            answer=entity.answer,
            display_order=entity.display_order,
            is_published=entity.is_published,
            view_count=entity.view_count,
            created_by=entity.created_by,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )