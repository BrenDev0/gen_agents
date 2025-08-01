from sqlalchemy.orm import Session
from src.api.core.repository.base_repository import BaseRepository
from src.api.core.logs.logger import Logger 
from src.api.modules.ai_config.ai_config_models import AIConfig, AiConfigCreate, AiConfigUpdate
from src.api.core.decorators.service_error_handler import service_error_handler
from uuid import UUID

class AiConfigService:
    _MODULE = "ai_config.service"
    def __init__(self, logger: Logger, repository: BaseRepository):
        self._logger = logger
        self._repository = repository

    @service_error_handler(module=_MODULE)
    def create(self, db: Session, ai_config: AiConfigCreate) -> AIConfig:
        return self._repository.create(db=db, data=AIConfig(**ai_config.model_dump(by_alias=False, exclude_unset=True)))

    @service_error_handler(module=_MODULE)
    def resource(self, db: Session, ai_config_id: UUID) -> AIConfig:
        return self._repository.get_one(db=db, key="ai_config_id", value=ai_config_id)
    
    @service_error_handler(module=_MODULE)
    def update(self, db: Session, ai_config_id: UUID, changes: AiConfigUpdate) -> AIConfig:
        return self._repository.update(db=db, key="ai_config_id", value=ai_config_id, changes=changes.model_dump(by_alias=False))
    
    @service_error_handler(module=_MODULE)
    def delete(self, db: Session, ai_config_id: UUID) -> AIConfig:
        return self._repository.delete(db=db, key="ai_config_id", value=ai_config_id)