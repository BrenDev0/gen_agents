# middleware/auth_middleware.py
from fastapi import Request, HTTPException
from core.dependencies.container import Container
from core.middleware.middleware_service import MiddlewareService
from fastapi.responses import JSONResponse

async def auth_middleware(request: Request):
    middleware_service: MiddlewareService = Container.resolve("middleware_service")
    user = middleware_service.auth(request)

    request.state.user = user
    return user
    
        