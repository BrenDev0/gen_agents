from sqlalchemy.orm import Session
from modules.embeddings.embeddings_dependencies import configure_embeddings_dependencies
from modules.messaging.messaging_dependencies import configure_messaging_dependencies
from modules.prompts.prompts_dependencies import configure_prompts_dependencies
from core.services.redis_service import RedisService
from core.services.webtoken_service import WebTokenService
from core.middleware.middleware_service import MiddlewareService
from core.dependencies.container import Container

def configure_container(db_session: Session):
    # core   
    redis_service = RedisService()
    Container.register("redis_service", redis_service)

    webtoken_service = WebTokenService()
    Container.register("webtoken_service", webtoken_service)

    middleware_service = MiddlewareService(
        webtoken_service=webtoken_service
    )
    Container.register("middleware_service", middleware_service)


    # embedding
    configure_embeddings_dependencies()

    # messaging
    configure_messaging_dependencies()

    # prompts
    configure_prompts_dependencies()






    





