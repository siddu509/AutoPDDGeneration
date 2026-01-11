"""
Utility functions for the PDD Generator application.
These are pure functions that eliminate code duplication across the codebase.
"""

import re
from typing import Optional, Callable

from app.core.config import get_logger

# Get module logger
logger = get_logger(__name__)


def strip_html_tags(text: str) -> str:
    """
    Remove HTML tags from text.

    This function is used to clean up HTML-formatted content
    and extract plain text. Used throughout the application.

    Args:
        text: String that may contain HTML tags

    Returns:
        Clean text without HTML tags, or default fallback if empty

    Example:
        >>> strip_html_tags("<p>Invoice Processing</p>")
        "Invoice Processing"
        >>> strip_html_tags("<strong>Bold</strong> text")
        "Bold text"
    """
    clean = re.sub('<[^<]+?>', '', text).strip()
    return clean if clean else "Process Design Document"


def safe_diagram_generation(diagram_func: Callable, process_steps: str) -> Optional[str]:
    """
    Generate diagram with error handling.

    Wraps diagram generation in try-except to prevent failures
    from breaking the entire PDD generation process.

    Args:
        diagram_func: Function that generates diagram code
        process_steps: Process steps content for diagram generation

    Returns:
        Diagram code string if successful, None if failed

    Example:
        >>> from app.agents.diagram_agent import generate_mermaid_diagram
        >>> code = safe_diagram_generation(generate_mermaid_diagram, steps_content)
        >>> if code:
        ...     print("Diagram generated")
        ... else:
        ...     print("Diagram generation failed, but PDD continues")
    """
    try:
        return diagram_func(process_steps)
    except Exception as e:
        logger.warning(f"Failed to generate diagram: {e}")
        return None


def extract_process_name(sections: list) -> str:
    """
    Extract and clean process name from sections list.

    The first section typically contains the process/project name.
    This function extracts it and removes any HTML formatting.

    Args:
        sections: List of section dictionaries with 'name' and 'content' keys

    Returns:
        Clean process name as plain text

    Example:
        >>> sections = [{"name": "Project Name", "content": "<p>Invoice Processing</p>"}]
        >>> extract_process_name(sections)
        "Invoice Processing"
    """
    if sections and sections[0].get("content"):
        return strip_html_tags(sections[0]["content"])
    return "Process Design Document"
