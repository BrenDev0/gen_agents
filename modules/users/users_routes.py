from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request
from core.dependencies.container import Container
from core.middleware.auth_middleware import auth_middleware
from core.middleware.verified_middleware import verified_middleware
from modules.users.users_controller import UsersController
from modules.users.users_models import UserCreate, UserUpdate, UserLogin
from sqlalchemy.orm import Session
from core.database.sessions import get_db_session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_controller() -> UsersController:
    controller: UsersController = Container.resolve("users_controller") 
    return controller

@router.post("/verified/create")
def verified_create(
    request: Request,
    data: UserCreate = Body(...),
    _=Depends(verified_middleware),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
    
):
    return controller.create_request(request=request, db=db, new_user=data)

@router.get("/secure/resource")
def secure_resource(
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    return controller.resource_request(request=request)

@router.put("/secure/update")
def secure_update(
    request: Request,
    data: UserUpdate = Body(...),
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    return controller.update_request(request=request, db=db, data=data)

@router.delete("/secure/delete")
def secure_delete(
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    return controller.delete_request(request=request, db=db)

@router.post("/login")
def login(
    request: Request,
    data: UserLogin = Body(...),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    return controller.login(request=request, db=db, data=data)
