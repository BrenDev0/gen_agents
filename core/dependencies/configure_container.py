from core.services.redis_service import RedisService
from core.services.webtoken_service import WebTokenService
from core.middleware.middleware_service import MiddlewareService
from core.dependencies.container import Container
from core.services.encryption_service import EncryptionService
from core.logs.logger import Logger
from core.services.hashing_service import HashingService
from core.services.request_validation_service import RequestValidationService
from core.services.http_service import HttpService
from modules.embeddings.embeddings_dependencies import configure_embeddings_dependencies
from modules.messaging.messaging_dependencies import configure_messaging_dependencies
from modules.prompts.prompts_dependencies import configure_prompts_dependencies
from modules.users.user_dependencies import configure_users_dependencies

def configure_container():
    # core   
    encryption_service = EncryptionService()
    Container.register("encryption_service", encryption_service)

    logger = Logger()
    Container.register("logger", logger)

    hashing_service = HashingService()
    Container.register("hashing_service", hashing_service)

    request_validatation_service = RequestValidationService()
    Container.register("request_validation_service", request_validatation_service)

    redis_service = RedisService()
    Container.register("redis_service", redis_service)

    webtoken_service = WebTokenService()
    Container.register("webtoken_service", webtoken_service)

    http_service = HttpService(
        encryption_service=encryption_service,
        logger=logger,
        hashing_service = hashing_service,
        request_validation_service=request_validatation_service,
        webtoken_service=webtoken_service
    )
    Container.register("http_service", http_service)

    middleware_service = MiddlewareService(
        http_service=http_service
    )
    Container.register("middleware_service", middleware_service)


    # embedding
    configure_embeddings_dependencies()

    # messaging
    configure_messaging_dependencies()

    # prompts
    configure_prompts_dependencies()

    # users 
    configure_users_dependencies(logger=logger)






    





