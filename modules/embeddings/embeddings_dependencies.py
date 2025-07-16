from sqlalchemy.orm import Session
from core.dependencies.container import Container
from modules.embeddings.embedding_service import EmbeddingService

def configure_embeddings_dependencies():
    service = EmbeddingService()
    Container.register("embeddings_service", service)