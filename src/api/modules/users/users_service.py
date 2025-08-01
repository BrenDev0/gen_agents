from src.api.modules.users.users_models import UserPublic, User, UserUpdate, UserCreate
from src.api.core.repository.base_repository import BaseRepository
from src.api.core.logs.logger import Logger
from sqlalchemy.orm import Session
from  typing import Dict, Any
from uuid import UUID
from src.api.core.decorators.service_error_handler import service_error_handler

class UsersService():
    _MODULE = "users.service" 
    def __init__(self, logger: Logger, repository: BaseRepository):
        self._repository = repository
        self._logger = logger

    @service_error_handler(module=_MODULE)
    def create(self, db: Session, user: UserCreate, email_hash: str, hashed_password: str) -> User:
        new_user = User(
            **user.model_dump(by_alias=False, exclude="code"),
            email_hash=email_hash
        )
        new_user.password = hashed_password

        return self._repository.create(db=db, data=new_user)

    @service_error_handler(module=_MODULE)
    def resource(self, db: Session, where_col: str, identifier: str | UUID) -> User | None:
        return self._repository.get_one(db=db, key=where_col, value=identifier)

    @service_error_handler(module=_MODULE)
    def update(self, db: Session, user_id: UUID, changes: UserUpdate) -> User:
        return self._repository.update(db, key="user_id", value=user_id, changes=changes)

    @service_error_handler(module=_MODULE)
    def delete(self, db: Session, user_id: UUID) -> User:
        return self._repository.delete(db=db, key="user_id", value=user_id)
