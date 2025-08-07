from src.api.core.services.redis_service import RedisService
from src.api.core.services.webtoken_service import WebTokenService
from src.api.core.middleware.middleware_service import MiddlewareService
from src.dependencies.container import Container
from src.api.core.services.encryption_service import EncryptionService
from src.api.core.logs.logger import Logger
from src.api.core.services.hashing_service import HashingService
from src.api.core.services.request_validation_service import RequestValidationService
from src.api.core.services.http_service import HttpService
from src.agent.services.embedding_service import EmbeddingService
from src.agent.services.prompt_service import PromptService
from src.api.modules.chats.chats_dependencies import configure_chats_dependencies
from src.api.modules.chats.messages.messages_dependencies import configure_messages_dependencies
from src.api.modules.users.user_dependencies import configure_users_dependencies
from src.api.modules.agents.agents_dependencies import configure_agents_dependencies
from src.agent.services.appointments_service import AppoinmentsService

def configure_container():
    ## core ##
    
    # Independents #    

    embeddings_service = EmbeddingService()
    Container.register("embeddings_service", embeddings_service)

    encryption_service = EncryptionService()
    Container.register("encryption_service", encryption_service)

    hashing_service = HashingService()
    Container.register("hashing_service", hashing_service)

    logger = Logger()
    Container.register("logger", logger)

    redis_service = RedisService()
    Container.register("redis_service", redis_service)

    request_validatation_service = RequestValidationService()
    Container.register("request_validation_service", request_validatation_service)

    webtoken_service = WebTokenService()
    Container.register("webtoken_service", webtoken_service)

    # Dependents # Must configure independent instances ablove this line #

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

    prompts_service = PromptService(
        embedding_service=embeddings_service,
        redis_service=redis_service
    )
    Container.register("prompts_service", prompts_service)

    appointments_service = AppoinmentsService(
        prompt_service=prompts_service
    )

    Container.register("appointments_service", appointments_service)

    ## Modules ## Must configure core instances above this line ##

    # agents 
    configure_agents_dependencies(logger=logger, http_service=http_service)
    
    # chats
    configure_chats_dependencies(logger=logger, http_service=http_service)
    
    # messages
    configure_messages_dependencies(logger=logger, http_service=http_service)

    # users 
    configure_users_dependencies(logger=logger, http_service=http_service)






    





