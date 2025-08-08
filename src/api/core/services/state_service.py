from src.api.core.services.redis_service import RedisService
from src.api.core.decorators.service_error_handler import service_error_handler
from sqlalchemy.orm import Session
from uuid import UUID
from   typing import List
from src.dependencies.container import Container
from src.api.modules.chats.messages.messages_models import Message
from src.api.modules.chats.messages.messages_service import MessagesService


class StateService:
    _MODULE = "state.service"
    def __init__(self, redis_service: RedisService):
        self._redis_service = redis_service

    @service_error_handler(module=_MODULE)
    async def get_state(self, db: Session, chat_id: UUID):
        pass


    @service_error_handler(module=_MODULE)
    async def ___get_chat_history(self, db: Session, chat_id: UUID, num_of_messages: int = 12) -> List[Message]:
        session_key = self._redis_service.get_agent_state_key(chat_id=chat_id)
    
        session_data = await self._redis_service.get_session(session_key)
        
        if session_data:
            chat_history = session_data.get("chat_history", [])
        else:
            messages_service: MessagesService = Container.resolve("messages_service")
            chat_history: List[Message] = messages_service.collection(db=db, chat_id=chat_id)[:num_of_messages]

        if len(chat_history) != 0:
            return chat_history
        
        return None
    
    @service_error_handler(module=_MODULE)
    async def __get_ai_config(self, db: Session, agent_id: UUID):
        ai_config_service = Container.resolve("ai_config_service")
        pass
    

        
