"""
Configuration Management
Loads settings from .env file and provides them to the application
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from backend directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """
    Application configuration class.
    Loads settings from environment variables with sensible defaults.
    """

    # Application
    APP_NAME: str = os.getenv("APP_NAME", "Shiina Mashiro")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Paths (create directories if they don't exist)
    SCREENSHOTS_DIR: Path = Path(os.getenv("SCREENSHOTS_DIR", "screenshots"))
    LOGS_DIR: Path = Path(os.getenv("LOGS_DIR", "logs"))

    # Browser
    DEFAULT_BROWSER_URL: str = os.getenv("DEFAULT_BROWSER_URL", "https://google.com")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_TO_FILE: bool = os.getenv("LOG_TO_FILE", "true").lower() == "true"
    LOG_TO_CONSOLE: bool = os.getenv("LOG_TO_CONSOLE", "true").lower() == "true"

    # Future: API Keys
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.SCREENSHOTS_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)

    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development mode."""
        return cls.ENVIRONMENT == "development"

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production mode."""
        return cls.ENVIRONMENT == "production"


# Create directories on import
Config.ensure_directories()

# Convenience instance for imports
config = Config()
