from src.dependencies.container import Container
from src.api.modules.agents.agents_controller import AgentsController
from src.api.modules.agents.agents_service import AgentsService
from src.api.modules.agents.agents_models import Agent
from src.api.core.services.http_service import HttpService
from src.api.core.repository.base_repository import BaseRepository
from src.api.core.logs.logger import Logger
def configure_agents_dependencies(logger:Logger, http_service: HttpService):
    repository = BaseRepository(Agent)
    service  = AgentsService(logger=logger, repository=repository)
  
    controller = AgentsController(
        http_service=http_service,
        agents_service=service
    )

    Container.register("agents_service", service)
    Container.register("agents_controller", controller)