"""
LLM Service for interacting with Language Learning Models.

This service encapsulates all LLM-related operations, including
section refinement and chat interactions. By centralizing LLM
calls, we make the code easier to test and maintain.
"""

from typing import Optional

from app.core.config import get_llm


class LLMService:
    """
    Service for LLM interactions.

    This service provides methods for common LLM operations used
    throughout the application, such as refining content and
    answering user questions.

    Example:
        >>> service = LLMService()
        >>> refined = service.refine_pdd_section(
        ...     "Purpose",
        ...     "Old content...",
        ...     "Make it more detailed"
        ... )
    """

    def refine_pdd_section(
        self,
        section_name: str,
        current_content: str,
        user_feedback: str
    ) -> str:
        """
        Refine a PDD section based on user feedback using AI.

        This method uses the LLM to rewrite section content based on
        user feedback, maintaining professional tone and UiPath standards.

        Args:
            section_name: Name of the section to refine
            current_content: Current section content
            user_feedback: User's feedback for improvement

        Returns:
            Refined section content

        Example:
            >>> service = LLMService()
            >>> refined = service.refine_pdd_section(
            ...     "Process Purpose",
            ...     "The purpose is to automate invoices.",
            ...     "Add more detail about business value"
            ... )
        """
        llm = get_llm()

        refine_prompt = f"""You are an expert UiPath Business Analyst refining a PDD section.

The section name is: '{section_name}'
The current content is: '{current_content}'
The user has provided the following feedback: '{user_feedback}'

Rewrite the section content based on the user's feedback.
- Maintain a professional tone
- Adhere to UiPath documentation standards
- Keep the content clear and concise
- Preserve the structure (bulleted lists, numbered steps, etc.) where appropriate

Output only the revised content, nothing else.
"""

        response = llm.invoke(refine_prompt)
        return response.content.strip()

    def chat_response(self, message: str, context: Optional[str] = None) -> str:
        """
        Generate AI response for clarification chat.

        Provides helpful responses to user questions about PDD creation,
        optionally using provided context about the process.

        Args:
            message: User's question or message
            context: Optional context about the process

        Returns:
            AI-generated response

        Example:
            >>> service = LLMService()
            >>> response = service.chat_response(
            ...     "What information do I need to provide?",
            ...     "Creating an invoice processing automation"
            ... )
        """
        llm = get_llm()

        if context:
            chat_prompt = f"""You are an expert UiPath Business Analyst helping a user create a Process Design Document (PDD).

Context about the process: {context}

User's question: {message}

Provide a helpful, concise response to assist with PDD creation.
If the question is about the process, use the provided context.
Keep responses focused on UiPath and RPA documentation standards.
"""
        else:
            chat_prompt = f"""You are an expert UiPath Business Analyst helping a user create a Process Design Document (PDD).

User's question: {message}

Provide a helpful, concise response to assist with PDD creation.
Keep responses focused on UiPath and RPA documentation standards.
"""

        response = llm.invoke(chat_prompt)
        return response.content.strip()
