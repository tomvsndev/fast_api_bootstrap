# FastAPI Production Starter Kit 🚀

A robust, production-ready FastAPI starter template designed for scalable, maintainable, and debuggable API development. This template provides a modular architecture with advanced logging, configuration management, background task support, and integration with `uv` for fast dependency management.

## 🌟 Key Features

### 🛠️ Production-Grade Configuration
- **Pydantic Settings Management**: Type-safe environment variable validation using Pydantic
- **Dual Mode Operation**: Development mode with auto-reload and production mode with multi-worker support
- **Host/IP Validation**: Secure host binding with comprehensive validation
- **Environment Variables**: Easy configuration via `.env` file with automatic validation

### 📊 Advanced Multi-Layer Logging System
- **Multi-Destination Logging**: Outputs to console, individual log files, complete log, and severity-based logs
- **Task-Specific Logging**: Each background task gets its own dedicated log file (e.g., `logs/SomeDemo.log`)
- **JSON Error Formatting**: Structured error logs with full traceback details for debugging
- **Color-Coded Console Output**: Developer-friendly colored logs for easier debugging
- **Log Rotation**: File size-based rotation with configurable backup management
- **Severity-Based Filtering**: Separate log files for WARNING, ERROR, and CRITICAL levels in `logs/severity/`
- **Complete Application Log**: All messages from all loggers in `logs/complete_log.log`

### 🔧 Background Task Management
- **Asynchronous Tasks**: Run custom background tasks with proper lifecycle management
- **Configurable Task Logging**: Each task can have its own logging level and dedicated log file
- **Lifespan Management**: Clean startup and shutdown using FastAPI's lifespan events
- **Extensible Task System**: Easily add custom tasks by extending the `BackgroundTask` class

### 🚀 Developer Experience
- **CORS Configuration**: Configurable Cross-Origin Resource Sharing via `.env`
- **Process Naming**: Clear process identification using `setproctitle`
- **Singleton Patterns**: Efficient resource management for logging and configuration
- **uv Integration**: Fast, modern dependency management with `uv` and `pyproject.toml`

## 🚀 Quick Start with uv (Recommended)

`uv` is a blazing-fast Python package installer and resolver written in Rust, ideal for managing modern Python projects.

### Installation

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup

1. **Clone the repository:**
```bash
git clone <your-repo>
cd fastapi-production-starter
```

2. **Create a virtual environment and install dependencies:**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
```

3. **Configure the environment:**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Run the application:**

**Development mode (with auto-reload):**
```bash
uv run main.py
```

**Production mode (with multiple workers):**
```bash
PRODUCTION=true uv run main.py
```

**Alternative (without activating venv):**
```bash
# Development mode
uv run --script main.py

# Production mode  
PRODUCTION=true uv run --script main.py
```

## 📁 Project Structure

```
├── main.py                 # Application entry point & task definitions
├── src/
│   ├── main/
│   │   └── main_setup.py   # FastAPI app factory and background task base class
│   ├── core/
│   │   └── fast_api_setup.py  # Configuration classes and FastAPI setup
│   └── utils/
│       └── logger.py       # Advanced logging system with JSON formatting
├── logs/                   # Log directory (auto-created)
│   ├── main.log           # Main application logs  
│   ├── complete_log.log   # All messages from all loggers
│   ├── SomeDemo.log       # Task-specific log files
│   └── severity/          # Severity-based logs
│       ├── warning.log
│       ├── error.log
│       └── critical.log
├── pyproject.toml          # Project dependencies and metadata
├── .env.example           # Environment variables template
└── README.md              # Project documentation
```

## ⚙️ Configuration

The application uses Pydantic for validated configuration via a `.env` file with two main configuration classes:

- **`MainConfig`**: Controls server operation (host, port, production mode, logging levels)
- **`FastApiConfig`**: Controls FastAPI app settings (title, description, CORS)

### Example .env File

```env
# Server Operation
PRODUCTION=false
HOST=0.0.0.0
PORT=8000
RELOAD=true
UVICORN_LOG_LEVEL=debug

# FastAPI Application  
SERVER_TITLE=My FastAPI Server
DESCRIPTION=Production-ready FastAPI application
VERSION=1.0.0
CORS_ORIGINS=*

# Component Logging Levels
MAIN_LOG_LEVEL=DEBUG
FASTAPI_LOG_LEVEL=DEBUG
```

### Configuration Validation

Both configuration classes include comprehensive validation:
- **Host validation**: Ensures valid IP addresses or localhost
- **Log level validation**: Accepts only valid logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Boolean conversion**: Automatically converts string values to booleans
- **Port validation**: Ensures ports are in valid range (1-65535)
- **CORS validation**: Validates CORS origin formats

## 📊 Advanced Logging System

### Logging Architecture

The logging system provides multiple output destinations for different purposes:

1. **Console Output**: Color-coded logs for development with JSON formatting for errors
2. **Task-Specific Files**: Each logger gets its own file (e.g., `logs/SomeDemo.log`)
3. **Complete Application Log**: All messages from all loggers in `logs/complete_log.log`
4. **Severity-Based Files**: Separate files for WARNING, ERROR, and CRITICAL in `logs/severity/`

### Logging Features

- **JSON Error Formatting**: ERROR and CRITICAL messages are formatted as JSON with full context
- **Log Rotation**: Automatic file rotation based on size with configurable backup count
- **Singleton Pattern**: Prevents duplicate loggers and handlers
- **Multi-Level Filtering**: Different formatters for console vs. file output
- **Exception Handling**: Full traceback capture with structured JSON output

### Usage Example

```python
from src.utils.logger import Logger, LoggerConfig

# Create logger manager (singleton)
logger_manager = Logger()

# Create custom logger configuration
logger_config = LoggerConfig(
    LOG_LEVEL="DEBUG",
    LOG_FILE="logs/my_service.log",
    ENABLE_SEVERITY_FILES=True,
    SEVERITY_FILES_DIR="logs/severity",
    MAX_LOG_SIZE_MB=10,
    BACKUP_COUNT=5
)

# Setup logger
logger = logger_manager.setup_logger(config=logger_config, logger_name="my_service")

# Use logger
logger.info("Service started")
logger.error("Something went wrong", exc_info=True)  # Will be JSON formatted
```

## 🔧 Background Tasks

The template supports asynchronous background tasks with proper lifecycle management and individual logging.

### Creating Background Tasks

Create tasks by extending the `BackgroundTask` base class:

```python
from src.main.main_setup import BackgroundTask, logger_manager
from src.utils.logger import LoggerConfig
import asyncio

class MyCustomTask(BackgroundTask):
    def __init__(self, logging_level='DEBUG'):
        # Setup task-specific logging
        self.logger_config = LoggerConfig(
            LOG_LEVEL=logging_level,
            LOG_FILE=f"logs/{self.__class__.__name__}.log",
            ENABLE_SEVERITY_FILES=True,
            SEVERITY_FILES_DIR="logs/severity"
        )
        self.logger = logger_manager.setup_logger(
            config=self.logger_config, 
            logger_name=self.__class__.__name__
        )

    async def run(self):
        """Task implementation - runs continuously"""
        while True:
            self.logger.info('Task is running')
            # Your task logic here
            await asyncio.sleep(5)
```

### Adding Tasks to Application

In `main.py`, add your task instances to the `background_tasks` list:

```python
# Create task instances
my_task = MyCustomTask(logging_level="INFO")
another_task = SomeOtherTask()

background_tasks = [
    my_task,
    another_task,
    # Add more BackgroundTask instances here
]
```

### Task Lifecycle Management

Tasks are automatically managed by FastAPI's lifespan context manager:
- **Startup**: All tasks are started as asyncio tasks when the app starts
- **Shutdown**: All tasks are cancelled and awaited when the app shuts down
- **Error Handling**: Exceptions during lifecycle events are logged and handled gracefully

## 🎯 FastAPI Application Factory

The application uses a factory pattern in `src/main/main_setup.py`:

### FastAPIApplication Class

```python
class FastAPIApplication:
    def __init__(self, config: MainConfig, background_tasks: List[BackgroundTask]):
        self.config = config
        self.background_tasks = background_tasks
        self.app = self._create_app()  # Creates the FastAPI instance

    def _create_app(self) -> FastAPI:
        """Create FastAPI application with lifespan"""
        return FastApiSetup(
            logger_manager=logger_manager,
            logging_level=config.FASTAPI_LOG_LEVEL
        ).app_create(lifespan=self.lifespan)
```

### Application Entry Point

The `main.py` file creates the app instance and runs it with uvicorn:

```python
# Create the FastAPI app instance
app_instance = FastAPIApplication(main_config, background_tasks)
app = app_instance.app  # This is what uvicorn imports

if __name__ == "__main__":
    # Run with import string to support reload/workers
    uvicorn.run(
        "main:app",  # Import string allows reload and multi-worker
        host=main_config.HOST,
        port=main_config.PORT,
        log_level=main_config.UVICORN_LOG_LEVEL.lower(),
        reload=not main_config.PRODUCTION,
        workers=4 if main_config.PRODUCTION else 1
    )
```

## 🔄 Development vs Production Modes

### Development Mode (`PRODUCTION=false`)
- **Auto-reload**: Code changes trigger automatic restarts
- **Single worker**: Easier debugging
- **Detailed logging**: More verbose console output
- **Debug-friendly**: Color-coded console logs

### Production Mode (`PRODUCTION=true`)
- **Multi-worker**: 4 workers by default for better performance
- **No auto-reload**: Stable operation
- **Optimized logging**: Reduced console verbosity
- **Process naming**: Clear process identification

## 🌐 CORS Configuration

Configure CORS in your `.env` file:

```env
# Allow all origins (development)
CORS_ORIGINS=*

# Allow specific origins (production)
CORS_ORIGINS=https://myapp.com,https://admin.myapp.com
```

## 🚀 Production Deployment

### Using systemd

Create `/etc/systemd/system/fastapi-service.service`:

```ini
[Unit]
Description=FastAPI Production Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
Environment=PRODUCTION=true
ExecStart=/path/to/.venv/bin/python -m uv run main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable fastapi-service
sudo systemctl start fastapi-service
sudo systemctl status fastapi-service
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY .env ./

# Install dependencies
RUN uv venv && uv sync

# Copy application code
COPY . .

EXPOSE 8000

# Run in production mode
ENV PRODUCTION=true
CMD ["uv", "run", "main.py"]
```

Build and run:
```bash
docker build -t fastapi-app .
docker run -d -p 8000:8000 --env-file .env fastapi-app
```

## 🛡️ Error Handling & Debugging

### Structured Exception Logging

The logging system captures full exception context:

```python
try:
    # Your code that might fail
    result = risky_operation()
except Exception as e:
    logger.exception(f"Operation failed: {str(e)}")
    # This will create a JSON-formatted error log with full traceback
```

### Log File Organization

For debugging, check these log files:
- **`logs/main.log`**: Main application logs
- **`logs/SomeDemo.log`**: Specific task logs  
- **`logs/complete_log.log`**: All messages from all loggers
- **`logs/severity/error.log`**: All ERROR messages across the application
- **`logs/severity/critical.log`**: All CRITICAL messages

### Debug Tips

1. **Task-specific debugging**: Each background task has its own log file
2. **Error aggregation**: Check `logs/severity/error.log` for all errors
3. **Complete overview**: Use `logs/complete_log.log` for full application flow
4. **JSON error format**: Errors include file, line number, function, and full traceback

## 📈 Performance & Best Practices

### Performance Tips
- Set `PRODUCTION=true` for multi-worker support (4 workers by default)
- Use appropriate log levels (`INFO` or higher in production)
- Task-specific log files enable faster debugging in large applications
- Log rotation prevents disk space issues

### Code Organization
- Extend `BackgroundTask` for new tasks
- Use the logger manager singleton to prevent duplicate handlers
- Configure logging levels per component via `.env`
- Use Pydantic validation for all configuration

### Resource Management
- Lifespan handlers ensure clean startup/shutdown
- Singleton patterns prevent resource duplication  
- Log rotation manages disk usage automatically
- Background tasks are properly cancelled on shutdown

## 🔧 Customization Examples

### Adding New Configuration Fields

Extend `MainConfig` or `FastApiConfig`:

```python
class MainConfig(BaseSettings):
    # Existing fields...
    
    DATABASE_URL: str = Field(
        default="sqlite:///./app.db",
        description="Database connection URL"
    )
    
    MAX_CONNECTIONS: int = Field(
        default=10,
        description="Maximum database connections"
    )
```

### Creating Custom Background Tasks

```python
class DatabaseCleanupTask(BackgroundTask):
    def __init__(self, interval_hours=24, logging_level='INFO'):
        self.interval_hours = interval_hours
        
        self.logger_config = LoggerConfig(
            LOG_LEVEL=logging_level,
            LOG_FILE=f"logs/{self.__class__.__name__}.log",
            ENABLE_SEVERITY_FILES=True,
            SEVERITY_FILES_DIR="logs/severity"
        )
        self.logger = logger_manager.setup_logger(
            config=self.logger_config, 
            logger_name=self.__class__.__name__
        )

    async def run(self):
        while True:
            try:
                self.logger.info("Starting database cleanup")
                # Your cleanup logic here
                await self.cleanup_old_records()
                self.logger.info("Database cleanup completed")
            except Exception as e:
                self.logger.exception(f"Database cleanup failed: {e}")
            
            await asyncio.sleep(self.interval_hours * 3600)
    
    async def cleanup_old_records(self):
        # Implementation here
        pass
```

### Adding API Routes

Create route modules and include them in the app:

```python
# In src/api/routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

# In main.py or app factory
app.include_router(router)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the existing patterns
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Configuration errors:**
- Check your `.env` file syntax
- Verify all required environment variables are set
- Review validation errors in the console output

**Logging issues:**
- Ensure the `logs/` directory is writable
- Check disk space for log files
- Verify log level configuration

**Task issues:**
- Check task-specific log files in `logs/`
- Verify task implementation follows the `BackgroundTask` pattern
- Check the complete log for task lifecycle events

### Getting Help

1. Check the specific log files for your issue
2. Review the `logs/complete_log.log` for full context
3. Verify your configuration matches the examples
4. Ensure you're using Python 3.9+ and have `uv` installed

## 🎯 Why Use This Template?

### 🚀 **Speed**: Bootstrap a production-ready FastAPI app with minimal setup
- Complete project structure ready to use
- Pre-configured logging, validation, and background tasks
- Development and production modes ready out of the box

### 📈 **Scalability**: Supports multi-worker deployments and extensible architecture  
- Multi-worker production mode
- Modular task system that scales with your needs
- Efficient resource management with singleton patterns

### 🔍 **Debuggability**: Task-specific logs and structured error handling
- Individual log files for each component
- JSON-formatted error logs with full context
- Severity-based log organization for quick issue identification

### 👨‍💻 **Developer-Friendly**: Modern tooling and excellent development experience
- Auto-reload in development mode
- Color-coded console output
- Fast dependency management with `uv`
- Type-safe configuration with Pydantic validation

### 🏭 **Production-Ready**: Robust logging, configuration, and deployment options
- Comprehensive error handling and logging
- Environment-based configuration
- Docker and systemd deployment examples
- Log rotation and resource management

---

**Happy coding with FastAPI and uv!** 🚀

This template provides everything you need to build scalable, maintainable, and debuggable FastAPI applications. The modular architecture grows with your project while maintaining clean separation of concerns and excellent observability through comprehensive logging.
