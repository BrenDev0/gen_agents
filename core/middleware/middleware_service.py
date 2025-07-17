import os
import jwt
from typing import Dict
from fastapi import Request, HTTPException
from core.services.webtoken_service import WebTokenService
from modules.users.users_service import UsersService
from core.dependencies.container import Container


class MiddlewareService:
    def __init__(self, webtoken_service: WebTokenService):
        self.TOKEN_KEY = os.getenv("TOKEN_KEY")
        self.webtoken_service = webtoken_service

    def get_token_payload(self, request: Request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unautrhorized, Missing required auth headers")
        
        token = auth_header.split(" ")[1]

        try:
            payload = self.webtoken_service.decode_token(token=token)

            return payload
        except jwt.ExpiredSignatureError:
            print("token expired")
            raise HTTPException(status_code=403, detail="Expired Token")
        
        except jwt.InvalidTokenError:
            print("token invalid")
            raise HTTPException(status_code=401, detail="Invlalid token")
        
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

        
    
    def auth(self, request: Request):
        token_payload = self.get_token_payload(request)
        user = self.authorize_user(token_payload)

        return user
    
    def verify(self, request: Request):
        token_payload = self.get_token_payload(request)

        verification_code = token_payload.get("verification_code")

        if verification_code is None:
            raise HTTPException(status_code=403, detail="Unauthorized")
        
        return verification_code


        
    
    def authorize_user(self, token_payload: Dict):
        try:  
            user_id = token_payload.get("user_id")

            if user_id is None:
                raise HTTPException(status_code=401, detail="Invlalid token")
            
            users_service: UsersService = Container.resolve("users_service") 
            user = users_service.resource(whereCol="user_id", identifier=user_id)

            if user is None:
                raise HTTPException(status_code=403, detail="Unauthorized")
            
            return user
    
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))


    

        

