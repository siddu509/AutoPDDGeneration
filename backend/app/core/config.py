"""
Configuration and dependency injection for the PDD Generator application.

This module centralizes all configuration settings and provides factory functions
for creating LLM clients and logging configuration. This eliminates duplication
and makes the application easier to test and maintain.

Configuration Priority:
1. Environment variables (highest priority)
2. config.yaml file
3. Default values (lowest priority)
"""

import os
import logging
import sys
from pathlib import Path
from functools import lru_cache
from typing import Optional

from langchain_openai import ChatOpenAI
from openai import OpenAI
import yaml


# Configuration class that loads from file and environment
class Config:
    """
    Application configuration loader.

    Loads configuration from multiple sources with priority:
    1. Environment variables (highest)
    2. config.yaml file
    3. Default values

    Example:
        >>> config = Config()
        >>> model = config.get("OPENAI_MODEL", "gpt-4o")
        >>> api_key = config.get("OPENAI_API_KEY")
    """

    def __init__(self):
        """Initialize configuration and load from config.yaml if exists."""
        self._config_data = {}
        self._load_from_file()

    def _load_from_file(self):
        """Load configuration from config.yaml file if it exists."""
        config_path = Path(__file__).parent.parent.parent / "config.yaml"

        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    self._config_data = yaml.safe_load(f) or {}
            except Exception as e:
                logging.warning(f"Failed to load config.yaml: {e}")

    def get(self, key: str, default=None):
        """
        Get configuration value with environment variable override.

        Priority: Environment variable > config.yaml > default

        Args:
            key: Configuration key (supports nested keys with dots, e.g., "openai.model")
            default: Default value if key not found

        Returns:
            Configuration value

        Example:
            >>> config = Config()
            >>> model = config.get("OPENAI_MODEL", "gpt-4o")
            >>> temperature = config.get("openai.temperature", 0.0)
        """
        # Try environment variable first
        env_value = os.getenv(key)
        if env_value is not None:
            return env_value

        # Try nested key access (e.g., "openai.model")
        keys = key.split('.')
        value = self._config_data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

        return value if value is not None else default


# Global config instance
_config = Config()


# Configure logging at module import time
def setup_logging(
    level: int = logging.INFO,
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) -> None:
    """
    Configure application-wide logging.

    This function should be called once at application startup to set up
    consistent logging across all modules.

    Args:
        level: Logging level (default: INFO)
        log_format: Format string for log messages

    Example:
        >>> setup_logging(logging.DEBUG)
        >>> logger = logging.getLogger(__name__)
        >>> logger.debug("Debug message")
    """
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


# Initialize logging on module import
setup_logging()


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.

    Factory function for getting loggers with consistent configuration.
    Use this instead of logging.getLogger() directly for consistency.

    Args:
        name: Usually __name__ from calling module

    Returns:
        Configured logger instance

    Example:
        >>> from app.core.config import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """
    return logging.getLogger(name)


@lru_cache()
def get_openai_api_key() -> str:
    """
    Get OpenAI API key from environment or config file.

    Uses lru_cache decorator to ensure the value
    is read only once and cached for performance.

    Returns:
        OpenAI API key string

    Example:
        >>> api_key = get_openai_api_key()
        >>> print(api_key[:10])  # First 10 characters
    """
    return _config.get("OPENAI_API_KEY", "")


@lru_cache()
def get_openai_model() -> str:
    """
    Get the OpenAI model to use for LLM operations.

    Reads from OPENAI_MODEL environment variable or config.yaml.

    Returns:
        Model name (default: gpt-4o)

    Example:
        >>> model = get_openai_model()
        >>> print(model)
        'gpt-4o'
    """
    return _config.get("OPENAI_MODEL", "gpt-4o")


@lru_cache()
def get_openai_temperature() -> float:
    """
    Get the OpenAI temperature setting.

    Returns:
        Temperature value (default: 0.0)

    Example:
        >>> temp = get_openai_temperature()
        >>> print(temp)
        0.0
    """
    temp_str = _config.get("OPENAI_TEMPERATURE", "0.0")
    try:
        return float(temp_str)
    except ValueError:
        return 0.0


@lru_cache()
def get_openai_api_base() -> Optional[str]:
    """
    Get the OpenAI API base URL.

    Returns:
        API base URL or None

    Example:
        >>> base = get_openai_api_base()
        >>> print(base)
        'https://api.openai.com/v1'
    """
    return _config.get("OPENAI_API_BASE")


def get_llm(
    model: str = None,
    temperature: float = None,
    api_key: str = None
) -> ChatOpenAI:
    """
    Get LangChain ChatOpenAI instance for LLM operations.

    This factory function eliminates duplication of LLM initialization
    across multiple endpoints and services.

    Args:
        model: Model name to use. If not provided, reads from config/env
        temperature: LLM temperature for generation. If not provided, reads from config/env
        api_key: Optional API key. If not provided, reads from environment

    Returns:
        Configured ChatOpenAI instance

    Example:
        >>> from app.core.config import get_llm
        >>> llm = get_llm()  # Uses configured model and temperature
        >>> response = llm.invoke("Hello, world!")
    """
    if model is None:
        model = get_openai_model()

    if temperature is None:
        temperature = get_openai_temperature()

    if api_key is None:
        api_key = get_openai_api_key()

    kwargs = {
        "model": model,
        "temperature": temperature,
        "api_key": api_key
    }

    # Add base_url if configured
    api_base = get_openai_api_base()
    if api_base:
        kwargs["base_url"] = api_base

    return ChatOpenAI(**kwargs)


def get_openai_client(api_key: str = None) -> OpenAI:
    """
    Get OpenAI client for direct API operations (e.g., Whisper transcription).

    This factory function provides the native OpenAI client for operations
    that aren't through LangChain (like audio transcription).

    Args:
        api_key: Optional API key. If not provided, reads from environment

    Returns:
        Configured OpenAI client instance

    Example:
        >>> from app.core.config import get_openai_client
        >>> client = get_openai_client()
        >>> transcription = client.audio.transcriptions.create(...)
    """
    if api_key is None:
        api_key = get_openai_api_key()

    kwargs = {"api_key": api_key}

    # Add base_url if configured
    api_base = get_openai_api_base()
    if api_base:
        kwargs["base_url"] = api_base

    return OpenAI(**kwargs)


@lru_cache()
def get_whisper_model() -> str:
    """
    Get the Whisper model name for audio transcription.

    Returns:
        Whisper model name (default: whisper-1)

    Example:
        >>> model = get_whisper_model()
        >>> print(model)
        'whisper-1'
    """
    return _config.get("WHISPER_MODEL", "whisper-1")


def get_app_config() -> dict:
    """
    Get application configuration from config.yaml.

    Returns the full application configuration dictionary.

    Returns:
        Configuration dictionary

    Example:
        >>> config = get_app_config()
        >>> print(config['app']['name'])
        'PDD Generator API'
    """
    return _config._config_data

