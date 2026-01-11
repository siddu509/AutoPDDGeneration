"""
Configuration and dependency injection for the PDD Generator application.

This module centralizes all configuration settings and provides factory functions
for creating LLM clients and logging configuration. This eliminates duplication
and makes the application easier to test and maintain.
"""

import os
import logging
import sys
from functools import lru_cache

from langchain_openai import ChatOpenAI
from openai import OpenAI


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
    Get OpenAI API key from environment.

    Uses lru_cache decorator to ensure the environment variable
    is read only once and cached for performance.

    Returns:
        OpenAI API key string

    Example:
        >>> api_key = get_openai_api_key()
        >>> print(api_key[:10])  # First 10 characters
    """
    return os.getenv("OPENAI_API_KEY", "")


def get_llm(
    model: str = "gpt-4o",
    temperature: float = 0.0,
    api_key: str = None
) -> ChatOpenAI:
    """
    Get LangChain ChatOpenAI instance for LLM operations.

    This factory function eliminates duplication of LLM initialization
    across multiple endpoints and services.

    Args:
        model: Model name to use (default: gpt-4o)
        temperature: LLM temperature for generation (default: 0.0)
        api_key: Optional API key. If not provided, reads from environment

    Returns:
        Configured ChatOpenAI instance

    Example:
        >>> from app.core.config import get_llm
        >>> llm = get_llm()
        >>> response = llm.invoke("Hello, world!")
    """
    if api_key is None:
        api_key = get_openai_api_key()

    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key
    )


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

    return OpenAI(api_key=api_key)
