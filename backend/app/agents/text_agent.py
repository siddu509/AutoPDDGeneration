import os
from pathlib import Path
from typing import List, Dict
import yaml

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_pdd_structure() -> Dict:
    """Load the PDD structure from the YAML file."""
    structure_path = Path(__file__).parent.parent / "core" / "pdd_structure.yaml"
    with open(structure_path, "r") as f:
        return yaml.safe_load(f)


def extract_pdd_sections(text_content: str) -> List[Dict[str, str]]:
    """
    Extract PDD sections from the provided text using GPT-4o.

    Args:
        text_content: The process description text to analyze

    Returns:
        A list of dictionaries with 'name' and 'content' keys for each PDD section

    Raises:
        Exception: If the OpenAI API call fails
    """
    try:
        # Initialize the OpenAI chat model
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )

        # Load the PDD structure
        pdd_structure = load_pdd_structure()
        sections = pdd_structure.get("sections", [])

        results = []

        # Process each section
        for section in sections:
            section_name = section["name"]
            section_prompt = section["prompt"]

            # Construct the full prompt for this section
            full_prompt = f"""{section_prompt}

Process Description:
{text_content}

Please provide the content for the '{section_name}' section based on the process description above.

IMPORTANT FORMATTING INSTRUCTIONS:
- Use HTML tags for formatting: <p> for paragraphs, <ul> and <li> for bulleted lists, <ol> and <li> for numbered lists
- Use <strong> for bold text and <em> for italic text
- DO NOT include markdown formatting (no **, no ##, no - for lists)
- DO NOT repeat the section name/title in your response - start directly with the content
- DO NOT include any preamble or introduction - start immediately with the actual content"""

            # Invoke the LLM
            response = llm.invoke(full_prompt)
            content = response.content

            results.append({
                "name": section_name,
                "content": content
            })

        return results

    except Exception as e:
        raise Exception(f"Error extracting PDD sections: {str(e)}")
