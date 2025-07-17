# middleware/auth_middleware.py
from fastapi import Request, HTTPException
from core.dependencies.container import Container
from core.middleware.middleware_service import MiddlewareService
from fastapi.responses import JSONResponse

def verified_middleware(request: Request):
    middleware_service: MiddlewareService = Container.resolve("middleware_service")
    verification_code = middleware_service.verify(request)

    request.state.verification_code = verification_code
    return verification_code
  
        