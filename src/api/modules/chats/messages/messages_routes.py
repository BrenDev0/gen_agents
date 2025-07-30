from fastapi import APIRouter, Depends, Request
from src.dependencies.container import Container
from typing import List
from src.api.core.middleware.auth_middleware import auth_middleware
from sqlalchemy.orm import Session
from src.api.core.database.sessions import get_db_session
from src.api.modules.chats.messages.messages_controller import MessagesController
from src.api.core.middleware.middleware_service import security
from src.api.modules.chats.messages.messages_models import MessagePublic
import uuid


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
    dependencies=[Depends(security)] 
)

def get_controller():
    return Container.resolve("messages_controller")

@router.get("/secure/collection/{chat_id}", status_code=200, response_model=List[MessagePublic])
def secure_collection( 
    chat_id: uuid.UUID,
    request: Request,
    _=Depends(auth_middleware), 
    db: Session = Depends(get_db_session),
    controller: MessagesController = Depends(get_controller)
):
    """
    ## Messages collection  request

    This endpoint returns a list of messages associated with the chat id passed in the params
    """
    return controller.collection_request(request=request, db=db, chat_id=chat_id)


    
