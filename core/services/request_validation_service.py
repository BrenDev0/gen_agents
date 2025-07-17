import uuid
from fastapi import HTTPException
from typing import List, Dict, Any
from core.dependencies.container import Container
from sqlalchemy.orm import Session

class RequestValidationService:
    def validate_uuid(self, uuid_str: str):
        try:
            uuid.UUID(uuid_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid id")
        
    def verify_resource(
        self,
        service_key: str,
        params: Dict[str, Any],
        not_found_message: str = "Resource not found" ,
        status_code: int = 404
    ):
        service = Container.resolve(service_key)

        result = service.resource(**params)

        if result is None:
            raise HTTPException(status_code=status_code, detail=not_found_message)
        
        return result