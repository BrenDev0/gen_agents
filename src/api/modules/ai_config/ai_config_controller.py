from src.api.modules.ai_config.ai_config_service import AiConfigService
from src.api.core.services.http_service import HttpService
from src.api.core.models.http_responses import GeneralResponse
from src.api.modules.ai_config.ai_config_models import AiConfigPublic, AiConfigUpdate, AiConfigCreate, AIConfig
from fastapi import Request
from sqlalchemy.orm import Session
from uuid import UUID

class AiConfigController:
    def __init__(self, http_service: HttpService, ai_config_service: AiConfigService):
        self._http_service = http_service
        self._ai_config_service = ai_config_service

    def create_request(self, request: Request, db: Session, data: AiConfigCreate) -> GeneralResponse:
        pass

    def resource_request(self, request: Request, db: Session, ai_config_id: UUID) -> AiConfigPublic:
        pass

    def update_request(self, request: Request, db: Session, ai_config_id: UUID, data: AiConfigUpdate) -> GeneralResponse:
        pass

    def delete_request(self, request: Request, db: Session, ai_config_id: UUID) -> GeneralResponse:
        pass


    def __to_public(ai_config: AIConfig) -> AiConfigPublic:
        pass