from modules.agents.agents_models import Agent, AgentCreate, AgentPublic, AgentPrivate, AgentUpdate
from core.repository.base_repository import BaseRepository
import logging
from core.logs.logger import Logger
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from uuid import UUID
from core.services.base_service import BaseService

class AgentsService(BaseService):
    def __init__(self, logger: Logger, repository: BaseRepository):
        super().__init__(logger=logger, module="agents.service")
        self.repository: BaseRepository = repository

    def create(self, db: Session,  agent: AgentPrivate) -> AgentPublic:
        return self.execute_with_handling("create", lambda: self.map_from_db(self.repository.create(db=db, data=self.map_to_db(agent))))

    def resource(self, db: Session, agent_id: UUID) -> AgentPublic | None:
        result = self.repository.get_one(db=db, key="agent_id", value=agent_id)
        if result is None:
            return None
        return self.map_from_db(result)
    
    def collection(self, db: Session, user_id: UUID) -> List[AgentPublic]:
        result = self.execute_with_handling("collection", lambda: self.repository.get_many(db=db, key="user_id", value=user_id))

        if len(result) != 0:
            return [self.map_from_db(agent).model_dump() for agent in result]
        return []
    
    def update(self, db: Session, agent_id: UUID, changes: Dict[str, Any]) -> AgentPublic:
        return self.execute_with_handling("update", lambda: self.map_from_db(self.repository.update(key="agent_id", value=agent_id, changes=changes)))

    def delete(self, db: Session, agent_id: UUID)-> AgentPublic:
        return self.execute_with_handling("delete", lambda: self.map_from_db(self.repository.delete(db=db, key="agent_id", value=agent_id)))
    
    @staticmethod
    def map_to_db(agent: AgentPrivate) -> Agent:
        return Agent(
            user_id=agent["userId"], 
            agent_name=agent.agentName,
            agent_description=agent.agentDescription
        )
    
    @staticmethod
    def map_from_db(agent: Agent) -> AgentPublic:
        return AgentPublic(
            agentId=agent.agent_id,
            userId=agent.user_id,
            agentName=agent.agent_name,
            agentDescription=agent.agent_description
        )
