from src.api.modules.agents.agents_models import Agent, AgentCreate, AgentPublic, AgentUpdate
from src.api.modules.chats.messages.messages_service import MessagesService
from src.api.modules.chats.messages.messages_models import Message
from src.api.core.repository.base_repository import BaseRepository
from src.dependencies.container import Container
from src.api.core.logs.logger import Logger
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from uuid import UUID
from src.api.core.services.redis_service import RedisService
from src.api.core.decorators.service_error_handler import service_error_handler

class AgentsService():
    _MODULE = "agents.service"
    def __init__(self, logger: Logger, repository: BaseRepository):
        self._repository: BaseRepository = repository
        self._logger = logger

    @service_error_handler(module=_MODULE)
    def create(self, db: Session,  agent: AgentCreate, user_id: UUID) -> Agent:
        new_agent = Agent(
            **agent.model_dump(by_alias=False),
            user_id = user_id
        )
        return self._repository.create(db=db, data=new_agent)

    @service_error_handler(module=_MODULE)
    def resource(self, db: Session, agent_id: UUID) -> Agent | None:
        result = self._repository.get_one(db=db, key="agent_id", value=agent_id)
        if result is None:
            return None
        return result
    
    @service_error_handler(module=_MODULE)
    def collection(self, db: Session, user_id: UUID) -> List[Agent]:
        result = self._repository.get_many(db=db, key="user_id", value=user_id)

        if len(result) != 0:
            return result
        return []
    
    @service_error_handler(module=_MODULE)
    def update(self, db: Session, agent_id: UUID, changes: AgentUpdate) -> Agent:
        return self._repository.update(db=db, key="agent_id", value=agent_id, changes=changes.model_dump(by_alias=False, exclude_unset=True))

    @service_error_handler(module=_MODULE)
    def delete(self, db: Session, agent_id: UUID)-> Agent:
        return self._repository.delete(db=db, key="agent_id", value=agent_id)


    @service_error_handler(module=_MODULE)
    async def get_agent_chat_history(self, db: Session, chat_id: UUID, num_of_messages: int = 12) -> List[Message]:
        redis_service: RedisService = Container.resolve("redis_service")
        session_key = redis_service.get_chat_history_key(chat_id=chat_id)
    
        session_data = await redis_service.get_session(session_key)
        
        if session_data:
            chat_history = session_data.get("chat_history", [])
        else:
            messages_service: MessagesService = Container.resolve("messages_service")
            chat_history: List[Message] = messages_service.collection(db=db, chat_id=chat_id)[:num_of_messages]
           
            await redis_service.set_session(session_key, {
                "chat_history": chat_history
            }, expire_seconds=7200)  # 2 hours

        if len(chat_history) != 0:
            return chat_history
        
        return None