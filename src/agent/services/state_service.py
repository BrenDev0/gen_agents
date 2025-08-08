from src.api.core.services.redis_service import RedisService
from src.api.core.decorators.service_error_handler import service_error_handler
from sqlalchemy.orm import Session
from uuid import UUID
from   typing import List
from src.dependencies.container import Container
from src.api.modules.chats.messages.messages_models import Message
from src.api.modules.chats.messages.messages_service import MessagesService
from src.api.modules.ai_config.ai_config_service import AiConfigService


class StateService:
    _MODULE = "state.service"
    def __init__(
        self, 
        redis_service: RedisService,
        messages_service: MessagesService,
        ai_config_service: AiConfigService
    ):
        self._redis_service = redis_service
        self._messages_service = messages_service
        self._ai_config_service = ai_config_service

    @service_error_handler(module=_MODULE)
    async def get_state(self, db: Session, chat_id: UUID):
        pass


    @service_error_handler(module=_MODULE)
    async def __get_chat_history(self, db: Session, chat_id: UUID, num_of_messages: int = 12) -> List[Message]:
        session_key = self._redis_service.get_agent_state_key(chat_id=chat_id)
    
        session_data = await self._redis_service.get_session(session_key)
        
        if session_data and session_data.get("chat_history"):
            return session_data["chat_history"][:num_of_messages]
        
        
        chat_history = self._messages_service.collection(db=db, chat_id=chat_id)
        return chat_history[:num_of_messages] if chat_history else []
    
    @service_error_handler(module=_MODULE)
    async def __get_ai_config(self, db: Session, agent_id: UUID):
        pass
    

        
