from fastapi import FastAPI
from pydantic import ValidationError,Field, field_validator
from starlette.middleware.cors import CORSMiddleware
import setproctitle

from src.utils.logger import LoggerConfig
from pydantic_settings import BaseSettings

class MainConfig(BaseSettings):
    """Main application configuration using Pydantic"""

    # Uvicorn server settings
    HOST: str = Field(
        default="0.0.0.0",
        description="Host to bind Uvicorn server to"
    )
    PORT: int = Field(
        default=8000,
        description="Port for Uvicorn server",
        ge=1,
        le=65535
    )
    RELOAD: bool = Field(
        default=False,
        description="Enable auto-reload for development"
    )
    UVICORN_LOG_LEVEL: str = Field(
        default="info",
        description="Uvicorn log level"
    )



    # Logging levels for different components
    MAIN_LOG_LEVEL: str = Field(
        default="INFO",
        description="Log level for main module"
    )
    FASTAPI_LOG_LEVEL: str = Field(
        default="INFO",
        description="Log level for FastAPI setup"
    )

    PRODUCTION:bool = Field(
        default="false",
        description="Production true will run uvicorn diff way"
    )
    class Config:
        env_file = ".env"
        env_prefix = ""
        case_sensitive = False

    @field_validator('HOST')
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host address"""
        import re

        valid_hosts = ['localhost', '0.0.0.0', '127.0.0.1']

        if v in valid_hosts:
            return v

        # Check if it's a valid IP address
        ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

        if re.match(ip_pattern, v):
            return v

        raise ValueError(f'Invalid HOST: {v}. Must be valid IP address or localhost')

    @field_validator('UVICORN_LOG_LEVEL', 'MAIN_LOG_LEVEL', 'FASTAPI_LOG_LEVEL')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate logging levels"""
        valid_levels = {'debug', 'info', 'warning', 'error', 'critical'}
        v_lower = v.lower()

        if v_lower not in valid_levels:
            raise ValueError(f'Invalid log level: {v}. Must be one of: {valid_levels}')

        return v_lower

    @field_validator('RELOAD')
    @classmethod
    def validate_reload(cls, v) -> bool:
        """Convert string to boolean for RELOAD"""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return bool(v)

    @field_validator('PRODUCTION')
    @classmethod
    def validate_production(cls, v) -> bool:
        """Convert string to boolean for RELOAD"""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on','false','no')
        return bool(v)

class FastApiConfig(BaseSettings):
    """Configuration class with Pydantic"""

    # Main app settings
    SERVER_TITLE: str = Field(
        default="python_server",
        description="Server title",
        min_length=1,
        max_length=50
    )
    DESCRIPTION: str = Field(
        default="Fast api description",
        description="Server description"
    )
    VERSION: str = Field(
        default="1.0.0",
        description="API version"
    )

    # FastAPI config
    HOST: str = Field(
        default="0.0.0.0",
        description="Host to bind to"
    )
    PORT: int = Field(
        default=8000,
        description="Port to listen on",
        ge=1,
        le=65535
    )
    CORS_ORIGINS: str = Field(
        default="*",
        description="CORS origins"
    )

    # Add logging configuration
    FASTAPI_LOG_LEVEL: str = Field(
        default="INFO",
        description="FastAPI logging level",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )

    class Config:
        env_file = ".env"
        env_prefix = ""  # No prefix for FastAPI config
        case_sensitive = False

    @field_validator('SERVER_TITLE')
    @classmethod
    def validate_server_title(cls, v: str) -> str:
        """Validate server title - SILENT validation"""
        if not v or v.strip() == "":
            raise ValueError('SERVER_TITLE cannot be empty')

        v = v.strip()
        invalid_chars = ['<', '>', '"', '&', "'"]
        if any(char in v for char in invalid_chars):
            raise ValueError(f'SERVER_TITLE contains invalid characters: {invalid_chars}')

        return v

    @field_validator('HOST')
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host address - SILENT validation"""
        import re

        valid_hosts = ['localhost', '0.0.0.0', '127.0.0.1']

        if v in valid_hosts:
            return v

        ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

        if re.match(ip_pattern, v):
            return v

        raise ValueError(f'Invalid HOST: {v}. Must be valid IP address or localhost')

    @field_validator('VERSION')
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate semantic version - SILENT validation"""
        import re

        version_pattern = r'^\d+\.\d+\.\d+$'

        if not re.match(version_pattern, v):
            raise ValueError(f'VERSION must follow semantic versioning (x.y.z): {v}')

        return v

    @field_validator('CORS_ORIGINS')
    @classmethod
    def validate_cors_origins(cls, v: str) -> str:
        """Validate CORS origins - SILENT validation"""
        if v == "*":
            return v

        origins = [origin.strip() for origin in v.split(',')]

        for origin in origins:
            if not origin.startswith(('http://', 'https://')):
                raise ValueError(f'CORS origin must start with http:// or https://: {origin}')

        return v

    @field_validator('FASTAPI_LOG_LEVEL')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level - SILENT validation"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Invalid log level: {v}. Must be one of {valid_levels}')
        return v.upper()

class FastApiSetup:
    # Class-level config instance to avoid multiple instantiations
    _config = None

    def __init__(self, logger_manager: object, logging_level=None):
        # Use singleton config
        self.config = FastApiSetup.get_config()

        # Use provided logging_level or fall back to config
        effective_log_level = logging_level or self.config.FASTAPI_LOG_LEVEL

        self.logger_config = LoggerConfig(
            LOG_LEVEL=effective_log_level,
            LOG_FILE=f"logs/{self.__class__.__name__}.log",
            ENABLE_SEVERITY_FILES=True,
            SEVERITY_FILES_DIR="logs/severity"
        )
        self.logger = logger_manager.setup_logger(config=self.logger_config, logger_name=self.__class__.__name__)

        # Log the effective logging level
        self.logger.debug(f"FastAPI logging level set to: {effective_log_level}")

    def set_process_title(self):
        """Set process title"""
        try:
            config = FastApiSetup.get_config()
            if config.SERVER_TITLE:
                setproctitle.setproctitle(config.SERVER_TITLE)
                self.logger.debug(f"Set process title to: {config.SERVER_TITLE}")
        except ValidationError as e:
            self.logger.error(f"Configuration validation failed: {e}")
            raise
        except Exception as e:
            self.logger.warning(f"Could not set process title: {e}")

    @classmethod
    def get_config(cls):
        """Get or create config instance - singleton pattern"""
        if cls._config is None:
            cls._config = FastApiConfig()
        return cls._config

    def app_create(self, lifespan) -> FastAPI:
        """Create FastAPI application with validated configuration"""
        try:
            # Set process title
            self.set_process_title()

            # Create FastAPI app
            app = FastAPI(
                lifespan=lifespan,
                title=self.config.SERVER_TITLE,
                description=self.config.DESCRIPTION,
                version=self.config.VERSION,
            )

            # Configure CORS
            cors_origins = ["*"] if self.config.CORS_ORIGINS == "*" else self.config.CORS_ORIGINS.split(',')

            app.add_middleware(
                CORSMiddleware,
                allow_origins=cors_origins,
                allow_credentials=True,
                allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                allow_headers=["*"],
            )

            self.logger.debug("FastAPI app created successfully")
            self.logger.debug(f"CORS origins: {cors_origins}")

            return app

        except ValidationError as e:
            self.logger.error("Configuration validation failed:")
            for error in e.errors():
                self.logger.error(f"  - {error['loc'][0]}: {error['msg']}")
            raise
        except Exception as e:
            self.logger.exception(f"Failed to create FastAPI app: {e}")
            raise