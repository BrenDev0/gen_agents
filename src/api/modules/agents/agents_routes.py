from fastapi import APIRouter, Depends, Body, Request
from src.dependencies.container import Container
from typing import List
from src.api.core.middleware.auth_middleware import auth_middleware
from sqlalchemy.orm import Session
from src.api.core.database.sessions import get_db_session
from src.api.modules.agents.agents_models import AgentCreate, AgentUpdate, AgentPublic
from src.api.core.models.http_responses import GeneralResponse
from src.api.modules.agents.agents_controller import AgentsController
import uuid
from src.api.core.middleware.middleware_service import security
from src.agent.graph import create_graph
from langchain_openai import ChatOpenAI


router = APIRouter(
    prefix="/agents",
    tags=["Agent"],
    dependencies=[Depends(security)] 
)

def get_controller():
    return Container.resolve("agents_controller")


def get_graph():
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.5
    )
    return create_graph(llm=llm)


@router.post("/secure/create", status_code=201, response_model=GeneralResponse)
def secure_create(
    requset: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller),
    data: AgentCreate = Body(...)
):
    """
    ## Create request 

    this endpoint creates an agent in the db
    **Required fields** - agentName
    **Optional fields** - agentDescription
    """
    return controller.create_request(requset=requset, db=db, data=data)


@router.get("/secure/resource/{agent_id}", status_code=200, response_model=AgentPublic)
def secure_resource(
    agent_id: uuid.UUID,
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller)
):
    """
    ## Resource request 

    this endpoint gets a single agent from the db by agentId in the params
    """
    return controller.resource_request(request=request, db=db, agent_id=agent_id)


@router.get("/secure/collection", status_code=200, response_model=List[AgentPublic])
def secure_collection(
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller)
):
    """
    ## Collection request 

    this endpoint returns a collection of agents based on the user id passed in the token   
    """
    return controller.collection_request(request=request, db=db)


@router.put("/secure/{agent_id}", status_code=200, response_model=GeneralResponse)
def secure_update(
    agent_id: uuid.UUID,
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller),
    data: AgentUpdate = Body(...)
):
    """
    ## Update request

    this endpoint updates the agents name or description
    """
    return controller.update_request(request=request, db=db, data=data, agent_id=agent_id)


@router.delete("/secure/{agent_id}", status_code=200, response_model=GeneralResponse)
def secure_delete(
    agent_id: uuid.UUID,
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller)
):
    """
    ## Delete request

    this endpoint deletes an agent by id
    """
    return controller.delete_request(request=request, db=db, agent_id=agent_id)
    

















# @router.post("/interact", response_class=JSONResponse)
# async def interact(
#     request: Request,
#     backgroundTasks: BackgroundTasks,
#     data: InteractionRequest = Body(...),
# ):
#     # user_id = request.state.user_id
#     # agent_service: AgentService = Container.resolve("agent_service")
#     # print(data)

#     # backgroundTasks.add_task(agent_service.interact, data.agent_id, data.conversation_id, user_id, data.input,)
#     redis_service: RedisService = Container.resolve("redis_service")
#     state = await redis_service.get_session(f"conversation_state:{data.conversation_id}")

#     llm = ChatOpenAI(
#             model="gpt-4o",
#             temperature=0.5
#         )
#     graph = create_graph(llm)
#     final_state = await graph.ainvoke(state)
    
#     return JSONResponse(status_code=200, content={"response": final_state["response"], "intent": final_state["intent"]});