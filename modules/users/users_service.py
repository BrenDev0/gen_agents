from modules.users.users_models import UserPublic, User, UserUpdate, UserPrivate
from core.repository.base_repository import BaseRepository
from core.dependencies.container import Container
from core.services.encryption_service import EncryptionService
import logging
from core.logs.logger import Logger
from typing import Dict, Any
from sqlalchemy.orm import Session
from uuid import UUID
from core.services.base_service import BaseService

class UsersService(BaseService): 
    def __init__(self, logger: Logger, repository: BaseRepository):
        super().__init__(logger=logger, module="users.service")
        self.repository = repository

    def create(self, db: Session, user: UserPrivate) -> UserPublic:
        return self.execute_with_handling("create", lambda: self.repository.create(db, self.map_to_db(user)))

    def resource(self, db: Session, where_col: str, identifier: str | UUID) -> User | None:
        return self.execute_with_handling("resource", lambda: self.repository.get_one(db, where_col, identifier))

    def update(self, db: Session, user_id: UUID, changes: UserUpdate) -> UserPublic:
        return self.execute_with_handling("update", lambda: self.map_from_db(
            self.repository.update(db, key="user_id", value=user_id, changes=changes)
        ))

    def delete(self, db: Session, user_id: UUID) -> UserPublic:
        return self.execute_with_handling("delete", lambda: self.map_from_db(
            self.repository.delete(db, key="user_id", value=user_id)
        ))

    @staticmethod
    def map_to_db(user: UserPrivate) -> User:
        encryption_service: EncryptionService = Container.resolve("encryption_service")
        return User(
            email=encryption_service.encrypt(user["email"]),
            email_hash=user["email_hash"],
            password=user["password"]
        )

    @staticmethod
    def map_from_db(user: User) -> UserPublic:
        encryption_service: EncryptionService = Container.resolve("encryption_service")
        return UserPublic(
            userId=str(user.user_id),
            email=encryption_service.decrypt(user.email)
        )
