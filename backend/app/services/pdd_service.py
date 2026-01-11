"""
PDD Service for generating and rendering Process Design Documents.

This service encapsulates all business logic related to PDD generation,
including section extraction, diagram generation, and HTML rendering.
By separating this logic from HTTP endpoints, we improve testability
and maintainability.
"""

from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Dict, List, Optional

from app.agents.text_agent import extract_pdd_sections
from app.agents.diagram_agent import generate_mermaid_diagram
from app.utils.helpers import extract_process_name, safe_diagram_generation


class PDDService:
    """
    Service for PDD generation and rendering.

    This class handles the core PDD generation workflow:
    1. Extract structured sections from process text
    2. Generate process flow diagram
    3. Render HTML output using Jinja2 template

    Attributes:
        template_path: Path to Jinja2 templates directory
        _env: Lazy-loaded Jinja2 Environment

    Example:
        >>> service = PDDService()
        >>> html = service.generate_pdd_html("Process description text...")
        >>> # or get structured data
        >>> data = service.generate_pdd_data("Process description...")
        >>> print(data['process_name'])
    """

    def __init__(self, template_path: Optional[Path] = None):
        """
        Initialize PDDService.

        Args:
            template_path: Path to templates directory. Defaults to app/templates
        """
        if template_path is None:
            template_path = Path(__file__).parent.parent / "templates"
        self.template_path = template_path
        self._env = None

    @property
    def env(self) -> Environment:
        """
        Lazy-loaded Jinja2 Environment.

        Uses property pattern to defer Environment creation
        until first use, improving startup time.

        Returns:
            Configured Jinja2 Environment

        Example:
            >>> service = PDDService()
            >>> env = service.env  # Created on first access
            >>> template = env.get_template("pdd_template.html")
        """
        if self._env is None:
            self._env = Environment(loader=FileSystemLoader(self.template_path))
        return self._env

    def generate_pdd_data(self, process_text: str) -> Dict:
        """
        Generate PDD data (sections and diagram) from process text.

        This is the core method that orchestrates PDD generation:
        - Extracts structured sections using text agent
        - Extracts and cleans process name
        - Generates Mermaid diagram code

        Args:
            process_text: Raw process description text

        Returns:
            Dictionary with keys:
                - process_name: Clean process name
                - sections: List of section dicts with 'name' and 'content'
                - diagram_code: Mermaid diagram code or None

        Example:
            >>> service = PDDService()
            >>> data = service.generate_pdd_data("Invoice process...")
            >>> print(data['process_name'])
            'Invoice Processing Automation'
            >>> print(len(data['sections']))
            10
        """
        sections = extract_pdd_sections(process_text)
        process_name = extract_process_name(sections)
        diagram_code = self._generate_diagram(sections)

        return {
            "process_name": process_name,
            "sections": sections,
            "diagram_code": diagram_code
        }

    def render_html_pdd(
        self,
        process_name: str,
        sections: List[Dict],
        diagram_code: Optional[str]
    ) -> str:
        """
        Render PDD as HTML using Jinja2 template.

        Args:
            process_name: Clean process name for title
            sections: List of section dictionaries
            diagram_code: Mermaid diagram code or None

        Returns:
            Rendered HTML string

        Example:
            >>> service = PDDService()
            >>> html = service.render_html_pdd(
            ...     "Invoice Process",
            ...     sections,
            ...     diagram_code
            ... )
        """
        template = self.env.get_template("pdd_template.html")
        return template.render(
            process_name=process_name,
            sections=sections,
            diagram_code=diagram_code
        )

    def generate_pdd_html(self, process_text: str) -> str:
        """
        Generate complete HTML PDD from process text.

        Convenience method that combines data generation and HTML rendering.

        Args:
            process_text: Raw process description text

        Returns:
            Complete HTML document ready for display or download

        Example:
            >>> service = PDDService()
            >>> html = service.generate_pdd_html("Process description...")
            >>> # Can return HTMLResponse(html) in FastAPI endpoint
        """
        data = self.generate_pdd_data(process_text)
        return self.render_html_pdd(
            data["process_name"],
            data["sections"],
            data["diagram_code"]
        )

    def _generate_diagram(self, sections: List[Dict]) -> Optional[str]:
        """
        Generate Mermaid diagram from process steps.

        Extracts the 6th section (Detailed Process Steps) and generates
        a flowchart diagram. Uses error handling to prevent failures.

        Args:
            sections: List of section dictionaries

        Returns:
            Mermaid diagram code string, or None if generation fails

        Example:
            >>> service = PDDService()
            >>> diagram = service._generate_diagram(sections)
            >>> if diagram:
            ...     print("Diagram generated successfully")
        """
        if len(sections) >= 6:
            process_steps = sections[5]["content"]
            return safe_diagram_generation(generate_mermaid_diagram, process_steps)
        return None
