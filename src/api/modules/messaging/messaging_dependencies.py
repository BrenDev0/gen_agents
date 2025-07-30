from sqlalchemy.orm import Session
from src.dependencies.container import Container
from src.api.modules.messaging.messaging_service import MessagingService

def configure_messaging_dependencies():
    service = MessagingService()
    Container.register("messaging_service", service)