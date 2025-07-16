from sqlalchemy.orm import Session
from core.dependencies.container import Container
from modules.messaging.messaging_service import MessagingService

def configure_messaging_dependencies():
    service = MessagingService()
    Container.register("messaging_service", service)