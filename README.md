FastAPI Production Starter Kit 🚀

A robust, production-ready FastAPI starter template designed for scalable, maintainable, and debuggable API development. This template provides a modular architecture with advanced logging, configuration management, background task support, and integration with uv for fast dependency management.

🌟 Features
🛠️ Production-Grade Configuration

Pydantic Settings Management: Type-safe environment variable validation using Pydantic.
Dual Mode Operation: Development mode with auto-reload and production mode with multi-worker support.
Host/IP Validation: Secure host binding with comprehensive validation.
Environment Variables: Easy configuration via .env file with prefix handling.

📊 Advanced Logging System

Multi-Destination Logging: Outputs to console, main log file, task-specific log files, and severity-based logs (WARNING, ERROR, CRITICAL).
JSON Error Formatting: Structured error logs with full traceback details.
Color-Coded Console Output: Developer-friendly colored logs for easier debugging.
Log Rotation: File size-based rotation with backup management.
Severity-Based Filtering: Separate log files for different severity levels in logs/severity/.
Task-Specific Logging: Background tasks (e.g., SomeDemo) have dedicated log files for faster debugging.

🔧 Background Task Management

Asynchronous Tasks: Run custom background tasks with proper lifecycle management (e.g., SomeDemo).
Configurable Logging: Each task can have its own logging level and dedicated log file, configurable via code or .env.
Lifespan Management: Clean startup and shutdown of tasks using FastAPI’s lifespan events.
Extensible Task System: Easily add custom tasks by extending the BackgroundTask class.

🚀 Developer Experience

CORS Configuration: Configurable Cross-Origin Resource Sharing via .env.
Process Naming: Clear process identification using setproctitle.
Singleton Patterns: Efficient resource management for logging and configuration.
uv Integration: Fast, modern dependency management with uv and pyproject.toml.


🚀 Quick Start with uv (Recommended)
uv is a blazing-fast Python package installer and resolver written in Rust, ideal for managing modern Python projects.
Installation
macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

Setup

Clone the repository:
git clone <your-repo>
cd fastapi-production-starter


Create a virtual environment and install dependencies:
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync


Configure the environment:
cp .env.example .env
# Edit .env with your settings


Run the application:

Development mode (with auto-reload):uv run main.py


Production mode (with multiple workers):PRODUCTION=true uv run main.py





Alternative (without activating venv):
# Development mode
uv run --script main.py

# Production mode
PRODUCTION=true uv run --script main.py


📁 Project Structure
├── main.py                 # Application entry point
├── src/
│   ├── main/
│   │   └── main_setup.py   # FastAPI app and configuration setup
│   ├── core/
│   │   └── fast_api_setup.py  # FastAPI configuration
│   ├── utils/
│   │   └── logger.py       # Advanced logging system
├── logs/                   # Log directory (auto-created)
│   ├── main.log
│   ├── fastapi.log
│   ├── SomeDemo.log        # Task-specific log file
│   └── severity/
│       ├── warning.log
│       ├── error.log
│       └── critical.log
├── pyproject.toml          # Project dependencies and metadata
├── .env.example            # Environment variables template
└── README.md               # Project documentation


⚙️ Configuration
The application uses Pydantic for validated configuration via a .env file.
Example .env File
# Server config
PRODUCTION=false
SERVER_TITLE=fastapi_server
DESCRIPTION=Your API Description
VERSION=1.0.0

# FastAPI config
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=*

# Uvicorn config
RELOAD=true
UVICORN_LOG_LEVEL=debug

# Component logging levels
MAIN_LOG_LEVEL=DEBUG
FASTAPI_LOG_LEVEL=DEBUG

Task-Specific Logging
Background tasks like SomeDemo can define their own logging levels and log files. For example:
class SomeDemo(BackgroundTask):
    def __init__(self, logging_level='DEBUG'):
        self.logger_config = LoggerConfig(
            LOG_LEVEL=logging_level,
            LOG_FILE=f"logs/{self.__class__.__name__}.log",
            ENABLE_SEVERITY_FILES=True,
            SEVERITY_FILES_DIR="logs/severity"
        )

You can override the logging level via code or add it to .env for task-specific configurations (e.g., SOMEDEMO_LOG_LEVEL=INFO).

📊 Logging System
Features

Multi-Handler Logging: Outputs to console, main log file, task-specific log files, and severity-based logs.
JSON Error Formatting: Structured error logs with tracebacks.
Color-Coded Output: Colorized console logs for development.
Log Rotation: Automatic rotation based on file size.
Severity-Based Logs: Separate files for WARNING, ERROR, and CRITICAL logs in logs/severity/.
Task-Specific Logs: Each background task can have its own log file (e.g., logs/SomeDemo.log) for easier debugging.

Usage Example
from src.utils.logger import Logger, LoggerConfig

logger_manager = Logger()
logger_config = LoggerConfig(
    LOG_LEVEL="DEBUG",
    LOG_FILE="logs/my_app.log",
    ENABLE_SEVERITY_FILES=True,
    SEVERITY_FILES_DIR="logs/severity"
)
logger = logger_manager.setup_logger(config=logger_config, logger_name="my_app")

logger.info("Application started")
logger.error("Something went wrong", exc_info=True)


🔧 Background Tasks
The template supports asynchronous background tasks with proper lifecycle management and task-specific logging.
Example: SomeDemo Task
from src.main.main_setup import BackgroundTask
from src.utils.logger import LoggerConfig
import asyncio

class SomeDemo(BackgroundTask):
    def __init__(self, logging_level='DEBUG'):
        self.logger_config = LoggerConfig(
            LOG_LEVEL=logging_level,
            LOG_FILE=f"logs/{self.__class__.__name__}.log",
            ENABLE_SEVERITY_FILES=True,
            SEVERITY_FILES_DIR="logs/severity"
        )
        self.logger = logger_manager.setup_logger(config=self.logger_config, logger_name=self.__class__.__name__)

    async def run(self):
        while True:
            self.logger.info('hello world')
            await asyncio.sleep(1)

Adding Tasks
In main.py, add task instances to the background_tasks list:
demo_task = SomeDemo(logging_level="INFO")
background_tasks = [demo_task]

Tasks are automatically started during app startup and stopped during shutdown via FastAPI’s lifespan.

🎯 FastAPI Setup
The FastAPI application is configured in src/main/main_setup.py with a modular FastAPIApplication class.
Example
from src.main.main_setup import FastAPIApplication

app_instance = FastAPIApplication(main_config, background_tasks)
app = app_instance.app

The app is run using Uvicorn with an import string ("main:app") to support auto-reload and multi-worker modes.

🔄 Lifespan Management
The application uses a lifespan context manager to handle startup and shutdown of tasks and resources.
Example
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    logger.info("Application starting up")
    yield
    logger.info("Application shutting down")


🌐 CORS Configuration
Configure CORS in the .env file:
# Allow specific origins
CORS_ORIGINS=https://frontend.com,https://admin.example.com

# Or allow all
CORS_ORIGINS=*


🚀 Production Deployment
Using systemd
Create /etc/systemd/system/fastapi-service.service:
[Unit]
Description=FastAPI Production Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
Environment=PRODUCTION=true
ExecStart=/path/to/uv run main.py
Restart=always

[Install]
WantedBy=multi-user.target

Run:
sudo systemctl enable fastapi-service
sudo systemctl start fastapi-service

Docker Deployment
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependencies
COPY pyproject.toml ./
RUN uv sync --frozen

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uv", "run", "main.py"]

Build and run:
docker build -t fastapi-app .
docker run -d -p 8000:8000 --env-file .env fastapi-app


🛡️ Error Handling
Use structured exception logging:
try:
    # Your code
except Exception as e:
    logger.exception(f"Operation failed: {str(e)}")


📈 Performance Tips

Use PRODUCTION=true in production for multi-worker support (4 workers by default).
Set appropriate log levels (INFO or higher) to reduce I/O overhead.
Use task-specific log files (e.g., logs/SomeDemo.log) for faster debugging in large applications.
Use uv for fast dependency resolution and reproducible builds.
Manage resources in lifespan handlers for efficient cleanup.
Avoid print statements; use the logger for consistent logging.


🔧 Customization
Adding Config Fields
Extend MainConfig in src/core/fast_api_setup.py:
from pydantic import BaseSettings, Field

class MainConfig(BaseSettings):
    NEW_FIELD: str = Field(default="default", description="New field")

Custom Log Formatting
Create a custom formatter:
from src.utils.logger import JsonFormatter

class CustomFormatter(JsonFormatter):
    def format(self, record):
        return super().format(record)

Adding Background Tasks
Create a new task by extending BackgroundTask:
class CustomTask(BackgroundTask):
    def __init__(self, logging_level='DEBUG'):
        self.logger_config = LoggerConfig(
            LOG_LEVEL=logging_level,
            LOG_FILE=f"logs/{self.__class__.__name__}.log",
            ENABLE_SEVERITY_FILES=True,
            SEVERITY_FILES_DIR="logs/severity"
        )
        self.logger = logger_manager.setup_logger(config=self.logger_config, logger_name=self.__class__.__name__)

    async def run(self):
        while True:
            self.logger.info("Custom task running")
            await asyncio.sleep(2)

Add to main.py:
custom_task = CustomTask(logging_level="INFO")
background_tasks.append(custom_task)


🤝 Contributing

Fork the repository.
Create a feature branch (git checkout -b feature/xyz).
Commit your changes (git commit -m 'Add xyz feature').
Push to the branch (git push origin feature/xyz).
Submit a pull request.


📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

🆘 Support

Check logs in logs/ (e.g., main.log, SomeDemo.log, severity/) for debugging.
Verify .env settings.
Ensure dependencies are installed with uv sync.
Python version: 3.9+.


🎯 Advantages

Modular Architecture: Separates configuration, app setup, and entry point for clean maintainability.
Task-Specific Logging: Each background task has its own log file (e.g., logs/SomeDemo.log), making debugging faster in large applications.
Uvicorn Compatibility: Uses "main:app" import string to support auto-reload and multi-worker modes without warnings.
Background Task Support: Easily integrate and manage asynchronous tasks with lifecycle handling.
Production-Ready: Robust logging, configuration, and deployment options for scalability.
uv-Powered Workflow: Fast dependency management with pyproject.toml and reproducible builds.
Debug-Friendly: Task-specific logs and severity-based logging simplify troubleshooting.


🚀 Why Use This Template?

Speed: Bootstrap a production-ready FastAPI app with minimal setup.
Scalability: Supports multi-worker deployments and extensible background tasks.
Debuggability: Task-specific logs and structured error handling make troubleshooting easy.
Developer-Friendly: Auto-reload, colored logs, and uv streamline development.
Modern Tooling: Leverages uv for fast, reliable dependency management.

Happy coding with FastAPI and uv! 🚀
