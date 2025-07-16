# app/repositories/base_repository.py
from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound

T = TypeVar("T") 

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, data: dict) -> T:
        instance = self.model(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get_one(self, key: str, value: str | int) -> Optional[T]:
        stmt = select(self.model).where(getattr(self.model, key) == value)
        result = self.db.execute(stmt).scalar_one_or_none()
        return result

    def get_many(self, key: str, value: str | int) -> List[T]:
        stmt = select(self.model).where(getattr(self.model, key) == value)
        return self.db.execute(stmt).scalars().all()

    def update(self, key: str, value: str | int, changes: dict) -> Optional[T]:
        stmt = update(self.model).where(getattr(self.model, key) == value).values(**changes).returning(self.model)
        result = self.db.execute(stmt)
        self.db.commit()
        return result.fetchone()

    def delete(self, key: str, value: str | int) -> Optional[T]:
        stmt = delete(self.model).where(getattr(self.model, key) == value).returning(self.model)
        result = self.db.execute(stmt)
        self.db.commit()
        return result.fetchone()
