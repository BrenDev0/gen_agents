from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request
from core.dependencies.container import Container
from core.middleware.auth_middleware import auth_middleware
from core.middleware.verified_middleware import verified_middleware
from modules.users.users_controller import UsersController


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

controller: UsersController = Container.resolve("users_controller") 

@router.get("/verified/create")
def verified_create(request: Request, _=Depends(verified_middleware)):
    return controller.create_request(request)

@router.get("/secure/resource")
def secure_resource(request: Request, _=Depends(auth_middleware)):
    return controller.resource_request(request)

