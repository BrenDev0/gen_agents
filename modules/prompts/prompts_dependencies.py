from sqlalchemy.orm import Session
from core.dependencies.container import Container
from modules.prompts.prompt_service import PromptService
from modules.embeddings.embedding_service import EmbeddingService

def configure_prompts_dependencies():
    service = PromptService()
    Container.register("prompts_service", service)