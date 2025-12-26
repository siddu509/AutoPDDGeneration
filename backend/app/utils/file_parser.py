"""
Document parsing utilities for extracting text from PDF and Word documents.
"""

import os
from typing import Optional
from pypdf import PdfReader
from docx import Document


def parse_document(file_path: str) -> str:
    """
    Parse a document (PDF or DOCX) and extract its text content.

    Args:
        file_path: Path to the document file

    Returns:
        Extracted text content as a string

    Raises:
        ValueError: If file type is not supported
        Exception: If file parsing fails
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.docx':
        return _parse_docx(file_path)
    elif file_extension == '.pdf':
        return _parse_pdf(file_path)
    else:
        raise ValueError(
            f"Unsupported file type: {file_extension}. "
            "Supported types: .pdf, .docx"
        )


def _parse_docx(file_path: str) -> str:
    """
    Extract text from a Word (.docx) document.

    Args:
        file_path: Path to the .docx file

    Returns:
        Extracted text content as a string
    """
    try:
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return '\n\n'.join(paragraphs)
    except Exception as e:
        raise Exception(f"Error parsing DOCX file: {str(e)}")


def _parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF document.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text content as a string

    Note:
        This function uses pypdf which works for text-based PDFs.
        For scanned PDFs (images), an OCR library like pytesseract would be needed.
    """
    try:
        reader = PdfReader(file_path)
        text_parts = []

        for page in reader.pages:
            text = page.extract_text()
            if text and text.strip():
                text_parts.append(text.strip())

        return '\n\n'.join(text_parts)
    except Exception as e:
        raise Exception(f"Error parsing PDF file: {str(e)}")
