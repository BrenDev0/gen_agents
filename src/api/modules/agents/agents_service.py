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
from src.agent.state import State, AppointmentState
from src.api.modules.ai_config.ai_config_service import AiConfigService

class AgentsService():
    _MODULE = "agents.service"
    def __init__(self, logger: Logger, repository: BaseRepository, redis_service: RedisService):
        self._repository: BaseRepository = repository
        self._logger = logger
        self._redis_service = redis_service

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

    
    

    
    