from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request
from src.dependencies.container import Container
from src.api.core.middleware.auth_middleware import auth_middleware
from src.api.core.middleware.verified_middleware import verified_middleware
from src.api.modules.users.users_controller import UsersController
from src.api.modules.users.users_models import UserCreate, UserUpdate, UserLogin, UserPublic, LoginResponse
from src.api.core.models.http_reposnses import GeneralResponse
from sqlalchemy.orm import Session
from src.api.core.database.sessions import get_db_session
from src.api.core.middleware.middleware_service import security

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_controller() -> UsersController:
    controller: UsersController = Container.resolve("users_controller") 
    return controller

@router.post("/verified/create", status_code=201, dependencies=[Depends(security)], response_model=GeneralResponse)
def verified_create(
    request: Request,
    data: UserCreate = Body(...),
    _=Depends(verified_middleware),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
    
):
    return controller.create_request(request=request, db=db, data=data)

@router.get("/secure/resource", status_code=200, response_model=UserPublic, dependencies=[Depends(security)])
def secure_resource(
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    return controller.resource_request(request=request)

@router.put("/secure/update", status_code=200, dependencies=[Depends(security)], response_model=GeneralResponse)
def secure_update(
    request: Request,
    data: UserUpdate = Body(...),
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    return controller.update_request(request=request, db=db, data=data)

@router.delete("/secure/delete", status_code=200, dependencies=[Depends(security)], response_model=GeneralResponse)
def secure_delete(
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    return controller.delete_request(request=request, db=db)

@router.post("/login", status_code=200, response_model=LoginResponse)
def login(
    request: Request,
    data: UserLogin = Body(...),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    return controller.login(request=request, db=db, data=data)
