from src.api.modules.agents.agents_service import AgentsService
from src.api.modules.agents.agents_models import AgentPublic, AgentCreate, AgentUpdate, Agent
from src.api.core.models.http_reposnses import GeneralResponse
from fastapi import Request
from src.api.core.services.http_service import HttpService
from sqlalchemy.orm import Session
from src.api.modules.users.users_models import User
import uuid
from typing import List

class AgentsController:
    def __init__(self, http_service: HttpService, agents_service: AgentsService):
        self._http_service = http_service
        self._agents_service = agents_service


    def create_request(self, requset: Request, db: Session, data: AgentCreate) -> GeneralResponse:
        user: User = requset.state.user

        self._agents_service.create(db=db, agent=data, user_id=user.user_id)

        return GeneralResponse(
            detail="Agent created"
        )
    

    def resource_request(self, request: Request, db: Session, agent_id: uuid.UUID) -> AgentPublic:
        user: User = request.state.user

        agent_resource: AgentPublic =  self._http_service.request_validation_service.verify_resource(
            "agents_service",
            {"db": db, "agent_id": agent_id},
            "Agent not found"
        )

        self._http_service.request_validation_service.validate_action_authorization(user.user_id, agent_resource.user_id)

        return self.__to_public(agent_resource)
    

    def collection_request(self, request: Request, db: Session) -> List[AgentPublic]:
        user: User = request.state.user

        data = self._agents_service.collection(db=db, user_id=user.user_id)

        return [self.__to_public(agent) for agent in data]
    

    def update_request(self, request: Request, db: Session, data: AgentUpdate, agent_id: uuid.UUID) -> GeneralResponse:
        user: User = request.state.user

        agent_resource: AgentPublic =  self._http_service.request_validation_service.verify_resource(
            "agents_service",
            {"db": db, "agent_id": agent_id},
            "Agent not found"
        )

        self._http_service.request_validation_service.validate_action_authorization(user.user_id, agent_resource.user_id)
    
        self._agents_service.update(db=db, agent_id=agent_resource.agent_id, changes=data)

        return GeneralResponse(
            detail="Agent updated"
        )
    

    def delete_request(self, request: Request, db: Session, agent_id: uuid.UUID) -> GeneralResponse:
        user: User = request.state.user

        agent_resource: AgentPublic =  self._http_service.request_validation_service.verify_resource(
            "agents_service",
            {"db": db, "agent_id": agent_id},
            "Agent not found"
        )

        self._http_service.request_validation_service.validate_action_authorization(user.user_id, agent_resource.user_id)

        self._agents_service.delete(db=db, agent_id=agent_resource.agent_id)

        return GeneralResponse(
            detail="Agent deleted"
        )
    

    @staticmethod
    def __to_public(agent: Agent) -> AgentPublic:
        return AgentPublic.model_validate(agent, from_attributes=True)
    



        