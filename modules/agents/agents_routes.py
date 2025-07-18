from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request
from core.dependencies.container import Container
from typing import List
from core.middleware.auth_middleware import auth_middleware
from sqlalchemy.orm import Session
from core.database.sessions import get_db_session
from modules.agents.agents_models import AgentCreate, AgentUpdate, AgentPublic
from modules.agents.agents_controller import AgentsController
import uuid
from core.middleware.middleware_service import security


router = APIRouter(
    prefix="/agents",
    tags=["Agent"],
    dependencies=[Depends(security)] 
)

def get_controller():
    return Container.resolve("agents_controller")


@router.post("/secure/create", status_code=201)
def secure_create(
    requset: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller),
    data: AgentCreate = Body(...)
):
    return controller.create_request(requset=requset, db=db, data=data)

@router.get("/secure/resource/{agent_id}", status_code=200, response_model=AgentPublic)
def secure_resource(
    agent_id: uuid.UUID,
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller)
):
    return controller.resource_request(request=request, db=db, agent_id=agent_id)

@router.get("/secure/collection", status_code=200, response_model=List[AgentPublic])
def secure_collection(
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller)
):
    return controller.collection_request(request=request, db=db)
    

















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