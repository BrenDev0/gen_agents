from modules.users.users_models import UserCreate, UserPublic, User, UserUpdate, UserPrivate
from core.repository.base_repository import BaseRepository
from core.dependencies.container import Container
from core.services.encryption_service import EncryptionService
import logging
from core.logs.logger import Logger
from typing import Dict, Any
from sqlalchemy.orm import Session
from uuid import UUID

class UsersService:
    def __init__(self, logger: Logger, repository: BaseRepository):
        self.logger: Logger = logger
        self.repository: BaseRepository = repository
        self.module = "users.service"

    def create(self, db: Session,  user: UserPrivate) -> UserPublic:
        try:
            mapped_user = self.map_to_db(user)

            new_user = self.repository.create(db=db, data=mapped_user)

            return new_user
        
        except Exception as e:
            self.logger.log(
                message=f"Error creating user",
                level=logging.ERROR,
                name=f"{self.module}.create",
                exc_info=True
            )
            raise


    def resource(self, db: Session, where_col: str, identifier: str | UUID)-> User | None:
        try:
            result = self.repository.get_one(db=db, key=where_col, value=identifier)
            
            # do not map result 
            return result
        
        except Exception as e:
            self.logger.log(
                message=f"Error getting user",
                level=logging.ERROR,
                name=f"{self.module}.resource",
                exc_info=True
            )
            raise

    def update(self, db: Session, user_id: UUID, changes: Dict[str, Any]) -> UserPublic:
        try:
            result = self.repository.update(
                db=db,
                key="user_id",
                value=user_id,
                changes=changes
            )

            return self.map_from_db(result)
        
        except Exception as e:
            self.logger.log(
                message=f"Error updating user",
                level=logging.ERROR,
                name=f"{self.module}.update",
                exc_info=True
            )
            raise

    def delete(self, db: Session, user_id: UUID)-> UserPublic:
        try:
            result = self.repository.delete(
                db=db,
                key="user_id",
                value=user_id
            )

            return self.map_from_db(result)
        
        except Exception as e:
            self.logger.log(
                message=f"Error deleting user",
                level=logging.ERROR,
                name=f"{self.module}.delete",
                exc_info=True
            )
            raise
    
    @staticmethod
    def map_to_db(user: UserPrivate) -> User:
        encryption_service: EncryptionService = Container.resolve("encryption_service")
        user = {
            "email": encryption_service.encrypt(user["email"]),
            "email_hash": user["email_hash"],
            "password": user["password"]
        }

        return user
    
    @staticmethod
    def map_from_db(user: User) -> UserPublic:
        encryption_service: EncryptionService = Container.resolve("encryption_service")
        return {
            "userId": str(user.user_id),
            "email": encryption_service.decrypt(user.email)
        }
