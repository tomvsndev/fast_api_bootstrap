import asyncio
import uvicorn
from src.main.main_setup import BackgroundTask, FastAPIApplication, main_config,logger_manager
from src.utils.logger import LoggerConfig

#you can import from anywhere main thing to have run in the class
class SomeDemo(BackgroundTask):
    def __init__(self,logging_level='DEBUG'):
        #add logger instance class based
        effective_log_level = logging_level
        self.logger_config = LoggerConfig(
            LOG_LEVEL=effective_log_level,
            LOG_FILE=f"logs/{self.__class__.__name__}.log",
            ENABLE_SEVERITY_FILES=True,
            SEVERITY_FILES_DIR="logs/severity"
        )
        self.logger = logger_manager.setup_logger(config=self.logger_config, logger_name=self.__class__.__name__)

    async def run(self):
        while True:
            self.logger.info('hello world')
            await asyncio.sleep(1)


# Create task instances
demo_task = SomeDemo()
background_tasks = [
    demo_task,
    # Add more BackgroundTask instances here
]

# Create the FastAPI app instance
app_instance = FastAPIApplication(main_config, background_tasks)
app = app_instance.app


if __name__ == "__main__":
    # Run Uvicorn with import string to support reload/workers
    uvicorn.run(
        "main:app",  # Import string for the app
        host=main_config.HOST,
        port=main_config.PORT,
        log_level=main_config.UVICORN_LOG_LEVEL.lower(),
        reload=not main_config.PRODUCTION,
        workers=4 if main_config.PRODUCTION else 1
    )