"""
Pydantic schemas for API request and response models.

This module contains all Pydantic models used for request validation
and response serialization. Centralizing these models makes them
reusable and easier to maintain.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class GeneratePDDRequest(BaseModel):
    """
    Request model for PDD generation from text.

    Attributes:
        process_text: Raw process description text

    Example:
        >>> request = GeneratePDDRequest(
        ...     process_text="The invoice process begins when..."
        ... )
    """
    process_text: str = Field(
        ...,
        description="The process description to generate a PDD from",
        example="The invoice processing process begins when an invoice is received via email. The finance clerk verifies the amount and approves it for payment."
    )


class PDDSection(BaseModel):
    """
    Model representing a single PDD section.

    Attributes:
        name: Section name/title
        content: Section content (may contain HTML)

    Example:
        >>> section = PDDSection(
        ...     name="Process Purpose",
        ...     content="<p>To automate invoice processing...</p>"
        ... )
    """
    name: str
    content: str


class RefineSectionRequest(BaseModel):
    """
    Request model for refining a PDD section.

    Attributes:
        section_name: Name of section to refine
        current_content: Current section content
        user_feedback: User's feedback for improvements

    Example:
        >>> request = RefineSectionRequest(
        ...     section_name="Process Purpose",
        ...     current_content="Old content...",
        ...     user_feedback="Make it more detailed"
        ... )
    """
    section_name: str
    current_content: str
    user_feedback: str


class ChatRequest(BaseModel):
    """
    Request model for chat interactions.

    Attributes:
        message: User's question or message
        context: Optional context about the process

    Example:
        >>> request = ChatRequest(
        ...     message="What information do I need?",
        ...     context="Creating an invoice processing automation"
        ... )
    """
    message: str
    context: Optional[str] = None


class ExportPDDRequest(BaseModel):
    """
    Request model for exporting PDD to different formats.

    Attributes:
        process_name: Name of the process
        sections: List of PDD sections
        diagram_code: Mermaid diagram code (optional)
        format: Export format ('html', 'docx', or 'pdf')

    Example:
        >>> request = ExportPDDRequest(
        ...     process_name="Invoice Processing",
        ...     sections=[...],
        ...     diagram_code="graph TD...",
        ...     format="docx"
        ... )
    """
    process_name: str
    sections: List[Dict[str, str]]
    diagram_code: Optional[str]
    format: str  # 'pdf', 'docx', or 'html'


class PDDResponse(BaseModel):
    """
    Response model for PDD generation JSON endpoint.

    Attributes:
        process_name: Clean process name
        sections: List of PDD sections
        diagram_code: Mermaid diagram code (optional)

    Example:
        >>> response = PDDResponse(
        ...     process_name="Invoice Processing",
        ...     sections=[...],
        ...     diagram_code="graph TD..."
        ... )
    """
    process_name: str
    sections: List[PDDSection]
    diagram_code: Optional[str]


class RefineSectionResponse(BaseModel):
    """
    Response model for section refinement.

    Attributes:
        refined_content: Refined section content

    Example:
        >>> response = RefineSectionResponse(
        ...     refined_content="Updated and improved content..."
        ... )
    """
    refined_content: str = Field(
        ...,
        description="The AI-refined content for the PDD section",
        example="<p>The updated process description with improvements based on your feedback...</p>"
    )


class ChatResponse(BaseModel):
    """
    Response model for chat interactions.

    Attributes:
        response: AI-generated response

    Example:
        >>> response = ChatResponse(
        ...     response="You need to provide the process steps..."
        ... )
    """
    response: str
