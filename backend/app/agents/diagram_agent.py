"""
Diagram generation agent for creating Mermaid.js flowcharts from process steps.
"""

from langchain_openai import ChatOpenAI

from app.core.config import get_llm


def generate_mermaid_diagram(process_steps: str) -> str:
    """
    Convert process steps into a Mermaid.js flowchart diagram.

    Args:
        process_steps: The detailed process steps content (from PDD section)

    Returns:
        Raw Mermaid.js code as a string

    Raises:
        Exception: If diagram generation fails
    """
    try:
        # Initialize LLM using centralized config
        llm = get_llm()

        # Create diagram generation prompt
        diagram_prompt = f"""
You are an expert in business process modeling.

Convert the following process steps into a Mermaid.js flowchart diagram.

Requirements:
- Use the `graph TD` (top-down) syntax
- Represent each step as a node (e.g., `A[Step 1]`)
- Represent decision points as diamond shapes (e.g., `B{{Is it valid?}}`)
- Use arrows (`-->`) to connect the nodes in sequence
- Keep the node text concise (max 3-4 words per node)
- Use clear, descriptive node IDs (A, B, C, etc.)
- For yes/no decisions, label the arrows like `-->|Yes|` and `-->|No|`
- Include a start node and end node
- ONLY output the valid Mermaid.js code, nothing else
- Do not include markdown formatting (no ```mermaid)

Process Steps:
{process_steps}

Output the Mermaid diagram code only:
"""

        # Generate diagram
        response = llm.invoke(diagram_prompt)
        mermaid_code = response.content.strip()

        # Clean up the response - remove markdown code blocks if present
        if mermaid_code.startswith("```"):
            # Remove markdown formatting
            lines = mermaid_code.split('\n')
            if lines[0].startswith("```mermaid"):
                lines = lines[1:]  # Remove first line
            elif lines[0].startswith("```"):
                lines = lines[1:]  # Remove first line
            if lines[-1].startswith("```"):
                lines = lines[:-1]  # Remove last line
            mermaid_code = '\n'.join(lines).strip()

        return mermaid_code

    except Exception as e:
        raise Exception(f"Error generating Mermaid diagram: {str(e)}")
