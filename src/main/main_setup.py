import asyncio
import sys
from contextlib import asynccontextmanager
from typing import List
from dotenv import load_dotenv

from src.core.fast_api_setup import MainConfig, FastApiSetup
from src.utils.logger import Logger, LoggerConfig


class BackgroundTask:
    """Base class for background tasks"""
    async def run(self) -> None:
        """Override this method to implement task logic"""
        raise NotImplementedError("Subclasses must implement run() method")


class FastAPIApplication:
    def __init__(self, config: MainConfig, background_tasks: List[BackgroundTask]):
        self.logger = logger
        self.config = config
        self.background_tasks = background_tasks
        self.app = self._create_app()

    def _create_app(self) -> FastApiSetup:
        """Create FastAPI application with lifespan"""
        return FastApiSetup(
            logger_manager=logger_manager,
            logging_level=logging_levels['fast_api']
        ).app_create(lifespan=self.lifespan)

    @asynccontextmanager
    async def lifespan(self, app):
        """FastAPI lifespan context manager"""
        try:
            self.logger.info("Application startup - starting background tasks")
            task_handles = [asyncio.create_task(task.run()) for task in self.background_tasks]
            yield
            self.logger.info("Application shutdown - cancelling background tasks")
            for task_handle in task_handles:
                task_handle.cancel()
            await asyncio.gather(*task_handles, return_exceptions=True)
        except Exception as e:
            self.logger.exception(f"Error during application lifecycle: {e}")
            raise


def setup_configuration() -> tuple:
    """Setup application configuration and logging"""
    load_dotenv()
    try:
        main_config = MainConfig()
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        sys.exit(1)

    logging_levels = {
        'fast_api': main_config.FASTAPI_LOG_LEVEL.upper(),
        'main': main_config.MAIN_LOG_LEVEL.upper(),
    }

    logger_config = LoggerConfig(
        LOG_LEVEL=logging_levels['main'],
        LOG_FILE="logs/main.log",
        ENABLE_SEVERITY_FILES=True,
        SEVERITY_FILES_DIR="logs/severity"
    )

    logger = logger_manager.setup_logger(config=logger_config, logger_name="main")
    return logger, logger_manager, logging_levels, main_config


# Configure logging
logger_manager = Logger()
if not logger_manager:
    sys.exit(0)

logger, logger_manager, logging_levels, main_config = setup_configuration()