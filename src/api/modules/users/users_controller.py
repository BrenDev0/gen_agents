from src.api.modules.users.users_service import UsersService
from src.api.modules.users.users_models import UserCreate, User, UserUpdate, UserLogin, UserPublic, LoginResponse
from src.api.core.models.http_reposnses import GeneralResponse
from fastapi import Request, HTTPException
from src.api.core.services.http_service import HttpService
from sqlalchemy.orm import Session
from src.dependencies.container import Container
from   src.api.core.services.encryption_service import EncryptionService

class UsersController:
    def __init__(self, https_service: HttpService, users_service: UsersService):
        self._http_service: HttpService = https_service
        self._users_service = users_service
        self._module = "users.controller"

    def create_request(self, request: Request, db: Session, data: UserCreate) -> GeneralResponse:
        verification_code = request.state.verification_code

        if data.code != verification_code:
            raise HTTPException(status_code=403, detail="Incorrect verification code")
        
        hashed_password = self._http_service.hashing_service.hash_password(password=data.password)
        hashed_email = self._http_service.hashing_service.hash_for_search(data=data.email)

        self._users_service.create(db=db, user=data, email_hash=hashed_email, hashed_password=hashed_password)
        
        return GeneralResponse(
            detail="User created"
        )
    

    
    def resource_request(self, request: Request) -> UserPublic:
        user: User = request.state.user

        data = self.__to_public(user=user)
        
        return data
        

    def update_request(self, request: Request, db: Session, data: UserUpdate) -> GeneralResponse:
        user: User = request.state.user 

        self._http_service.hashing_service.compare_password(data.old_password, user.password)
        hashed_password = self._http_service.hashing_service.hash_password(data.new_password)
    

        self._users_service.update(
            db=db,
            user_id=user.user_id, 
            changes={"password": hashed_password}
        )

        return GeneralResponse(
            detail="User updated"
        )

    def delete_request(self, request: Request, db: Session) -> GeneralResponse:
        user: User = request.state.user

        self._users_service.delete(
            db=db,
            user_id=user.user_id
        )

        return GeneralResponse(
            detail="User deleted"
        )
    
    def login(self, request: Request, db: Session, data: UserLogin) -> LoginResponse: 
        hashed_email = self._http_service.hashing_service.hash_for_search(data=data.email)
        
        user: User = self._http_service.request_validation_service.verify_resource(
            service_key="users_service",
            params={"db": db, "where_col": "email_hash", "identifier": hashed_email},
            not_found_message="User not found",
        )

        self._http_service.hashing_service.compare_password(data.password, user.password)

        token = self._http_service.webtoken_service.generate_token({
            "user_id": str(user.user_id)
        }, "7d")

        return LoginResponse(
            token=token
        )


    @staticmethod
    def __to_public(user: User) -> UserPublic:
        encryptionService: EncryptionService = Container.resolve("encryption_service")
        return UserPublic(
            user_id=str(user.user_id),
            email=encryptionService.decrypt(user.email)
        )
