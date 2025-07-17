from .users_models import UserCreate, UserResponse, User
from core.repository.base_repository import BaseRepository
from core.dependencies.container import Container
from core.services.encryption_service import EncryptionService

class UsersService:
    def __init__(self, repository: BaseRepository):
        self.repository: BaseRepository = repository(User)

    def create(self, user: UserCreate) -> UserResponse:
        mapped_user = self.map_to_db(user)

        new_user = self.repository.create(mapped_user)

        return new_user


    def resource(self, whereCol: str, identifier: str)-> UserResponse | None:
        result = self.repository.get_one(whereCol, identifier)

        if not result:
            return None

        return self.map_from_db(result)

    def update(self, user_id: str) -> UserResponse:
        pass

    def delete(self, user_id: str)-> UserResponse:
        pass

    def map_to_db(user: UserCreate) -> User:
        encryption_service: EncryptionService = Container.resolve("encryption_service")
        user = {
            "email": encryption_service.encrypt(user.email),
            "password": user.password
        }

        return user
    
    def map_from_db(user: User) -> UserResponse:
        encryption_service: EncryptionService = Container.resolve("encryption_service")
        return {
            "userId": user.user_id,
            "email": encryption_service.decrypt(user.email)
        }
