from datetime import datetime
from typing import Optional, Type, TypeVar

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Mapped, Session, declarative_mixin, declared_attr

from todorate.database import Base

ModelType = TypeVar("ModelType", bound="BaseDBModel")


@declarative_mixin
class BaseDBModel:
    """Generic model providing base functionality used by all models.

    Must be inherited from in addition to Base.
    """

    @declared_attr
    def date_created(cls) -> Mapped[datetime]:
        return Column(DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def date_modified(cls) -> Mapped[datetime]:
        return Column(DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def is_deleted(cls) -> Mapped[datetime]:
        return Column(Boolean, nullable=False, default=False, index=True)

    @classmethod
    def get_by_id(
        cls: Type[ModelType], session: Session, id: str
    ) -> Optional[ModelType]:
        try:
            return session.query(cls).filter_by(id=id).first()
        except DataError:
            return None

    def set_modified(self) -> None:
        self.date_modified = datetime.utcnow()


__all__ = ["Base", "BaseDBModel"]
