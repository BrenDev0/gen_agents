from modules.users.users_service import UsersService
from modules.users.users_models import UserCreate
from fastapi import BackgroundTasks, Depends, Body, Request, HTTPException
from fastapi.responses import JSONResponse

class UsersController:
    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    def create_request(self, request: Request, new_user: UserCreate = Body(...)):
        verification_code = request.state.verification_code

        if new_user.code != verification_code:
            raise HTTPException(status_code=403, detail="Incorrect verification code")
        
        self.users_service.create(new_user)
        
        return JSONResponse(status_code=201, 
            content={
                "message": "User created"
            }
        );
 
    


    def resource_request(self, request: Request):
        user = request.state.user
        return JSONResponse(status_code=200, 
            content={
                "data": user
            }
        );
        

    def update_request(self):
        pass

    def delete_request(self):
        pass