from src.api.modules.chats.chats_models import Chat, ChatPublic
from src.api.modules.users.users_models import User
from src.api.modules.chats.chats_service import ChatsService
from src.api.modules.chats.chats_models import  Chat, ChatCreate, ChatCreateResposne, ChatUpdate
from src.api.core.models.http_responses import GeneralResponse
from fastapi import Request
from src.api.core.services.http_service import HttpService
from sqlalchemy.orm import Session
from typing import List
import uuid
from src.api.modules.users.users_models import User


class ChatsController:
    def __init__(self, https_service: HttpService, chats_service: ChatsService):
        self._http_service: HttpService = https_service
        self._chats_service = chats_service
        self._module = "chats.controller"

    def create_request(self, request: Request, db: Session) -> ChatCreateResposne:
        user: User = request.state.user

        chat = self._chats_service.create(db=db, chat=ChatCreate(
            user_id=user.user_id
        ))

        return ChatCreateResposne(
            chatId=chat.chat_id
        )
 
    def collection_request(self, request: Request, db: Session) -> List[ChatPublic]:
        user: User = request.state.user

        data = self._chats_service.collection(db=db, user_id=user.user_id)
        
        return [self.__to_public(chat) for chat in data]

    def update_request(self, request: Request, db: Session, data: ChatUpdate, chat_id: uuid.UUID) -> GeneralResponse:
        user: User = request.state.user

        chat_resource: Chat = self._http_service.request_validation_service.verify_resource(
            service_key="chats_service",
            params={"db": db, "chat_id": chat_id},
            not_found_message="Chat not found"
        )  

        self._http_service.request_validation_service.validate_action_authorization(user.user_id, chat_resource.user_id) 

        self._chats_service.update(db=db, chat_id=chat_resource.chat_id, changes=data)

        return GeneralResponse(
            detail="Chat updated"
        )
   
    @staticmethod
    def __to_public(chat: Chat) -> ChatPublic:
        return ChatPublic.model_validate(chat, from_attributes=True)
        