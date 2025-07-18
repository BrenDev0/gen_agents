# core/services/base_service.py
from core.logs.logger import Logger
import logging

class BaseService:
    def __init__(self, logger: Logger, module: str):
        self.logger = logger
        self.module = module

    def execute_with_handling(self, method: str, func):
        try:
            return func()
        except Exception as e:
            self.logger.log(
                message=f"Error in {method}",
                level=logging.ERROR,
                name=f"{self.module}.{method}",
                exc_info=True
            )
            raise
