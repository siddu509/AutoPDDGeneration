"""
API endpoints for the PDD Generator application.

This module contains all HTTP endpoints for the application.
After refactoring, endpoints are thin controllers that delegate
business logic to the service layer.
"""

from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from typing import Optional

from app.api.schemas import (
    GeneratePDDRequest,
    RefineSectionRequest,
    ChatRequest,
    ExportPDDRequest
)
from app.services.pdd_service import PDDService
from app.services.llm_service import LLMService
from app.services.file_processing_service import FileProcessingService
from app.services.export_service import ExportService


router = APIRouter()


# ==================== Dependency Injection ====================

def get_pdd_service() -> PDDService:
    """Dependency injection for PDDService."""
    return PDDService()


def get_llm_service() -> LLMService:
    """Dependency injection for LLMService."""
    return LLMService()


def get_file_processing_service() -> FileProcessingService:
    """Dependency injection for FileProcessingService."""
    return FileProcessingService()


def get_export_service() -> ExportService:
    """Dependency injection for ExportService."""
    return ExportService()


# ==================== HTML Endpoints ====================

@router.post("/generate-pdd", response_class=HTMLResponse)
async def generate_pdd(
    request: Request,
    body: GeneratePDDRequest,
    pdd_service: PDDService = Depends(get_pdd_service)
):
    """
    Generate a PDD from the provided process text and return as HTML.

    Args:
        request: FastAPI request object
        body: Request body containing process_text
        pdd_service: Injected PDDService instance

    Returns:
        HTMLResponse with the rendered PDD

    Raises:
        HTTPException: If PDD generation fails
    """
    try:
        html_content = pdd_service.generate_pdd_html(body.process_text)
        return HTMLResponse(content=html_content)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDD: {str(e)}"
        )


@router.post("/upload-and-process", response_class=HTMLResponse)
async def upload_and_process(
    request: Request,
    file: UploadFile = File(...),
    file_service: FileProcessingService = Depends(get_file_processing_service),
    pdd_service: PDDService = Depends(get_pdd_service)
):
    """
    Upload a file (PDF, DOCX, or MP4) and generate a PDD from its content as HTML.

    For documents (PDF, DOCX): Extracts text and processes it.
    For videos (MP4): Transcribes audio and analyzes frames.

    Args:
        request: FastAPI request object
        file: Uploaded file
        file_service: Injected FileProcessingService instance
        pdd_service: Injected PDDService instance

    Returns:
        HTMLResponse with the rendered PDD

    Raises:
        HTTPException: If file processing fails
    """
    try:
        content = await file.read()
        process_text, _ = await file_service.process_upload(content, file.filename)

        html_content = pdd_service.generate_pdd_html(process_text)
        return HTMLResponse(content=html_content)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process file: {str(e)}"
        )
    finally:
        file_service.cleanup()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# ==================== Interactive Endpoints ====================

@router.post("/refine-section")
async def refine_section(
    request: Request,
    body: RefineSectionRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Refine a PDD section based on user feedback using AI.

    Args:
        request: FastAPI request object
        body: Request containing section_name, current_content, and user_feedback
        llm_service: Injected LLMService instance

    Returns:
        JSONResponse with refined content

    Raises:
        HTTPException: If refinement fails
    """
    try:
        refined_content = llm_service.refine_pdd_section(
            body.section_name,
            body.current_content,
            body.user_feedback
        )

        return {"refined_content": refined_content}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refine section: {str(e)}"
        )


@router.post("/chat")
async def chat(
    request: Request,
    body: ChatRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Clarification chat endpoint for asking questions about PDD generation.

    Args:
        request: FastAPI request object
        body: Request containing message and optional context
        llm_service: Injected LLMService instance

    Returns:
        JSONResponse with AI response

    Raises:
        HTTPException: If chat fails
    """
    try:
        ai_response = llm_service.chat_response(body.message, body.context)
        return {"response": ai_response}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat: {str(e)}"
        )


# ==================== JSON API Endpoints for Interactive UI ====================

@router.post("/api/generate-pdd-json")
async def generate_pdd_json(
    request: Request,
    body: GeneratePDDRequest,
    pdd_service: PDDService = Depends(get_pdd_service)
):
    """
    Generate a PDD and return structured JSON (for interactive UI).

    Args:
        request: FastAPI request object
        body: Request body containing process_text
        pdd_service: Injected PDDService instance

    Returns:
        JSONResponse with sections and diagram code

    Raises:
        HTTPException: If PDD generation fails
    """
    try:
        data = pdd_service.generate_pdd_data(body.process_text)
        return data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDD: {str(e)}"
        )


@router.post("/api/upload-and-process-json")
async def upload_and_process_json(
    request: Request,
    file: UploadFile = File(...),
    file_service: FileProcessingService = Depends(get_file_processing_service),
    pdd_service: PDDService = Depends(get_pdd_service)
):
    """
    Upload a file and return structured JSON (for interactive UI).

    Args:
        request: FastAPI request object
        file: Uploaded file
        file_service: Injected FileProcessingService instance
        pdd_service: Injected PDDService instance

    Returns:
        JSONResponse with sections and diagram code

    Raises:
        HTTPException: If file processing fails
    """
    try:
        content = await file.read()
        process_text, _ = await file_service.process_upload(content, file.filename)

        data = pdd_service.generate_pdd_data(process_text)
        return data

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process file: {str(e)}"
        )
    finally:
        file_service.cleanup()


# ==================== Export Endpoint ====================

@router.post("/api/export-pdd")
async def export_pdd(
    request: Request,
    body: ExportPDDRequest,
    export_service: ExportService = Depends(get_export_service)
):
    """
    Export PDD as PDF, Word, or HTML document.

    Args:
        request: FastAPI request object
        body: Request containing PDD data and format
        export_service: Injected ExportService instance

    Returns:
        StreamingResponse with the document file

    Raises:
        HTTPException: If export fails
    """
    try:
        if body.format == 'html':
            # Generate HTML
            html_content = export_service.create_html_document(
                body.process_name,
                body.sections,
                body.diagram_code
            )

            # Return as downloadable file
            return StreamingResponse(
                iter([html_content]),
                media_type="text/html",
                headers={
                    "Content-Disposition": f"attachment; filename=PDD_{body.process_name.replace(' ', '_')}.html"
                }
            )

        elif body.format == 'docx':
            # Generate Word document
            doc_bytes = export_service.create_word_document(
                body.process_name,
                body.sections,
                body.diagram_code
            )

            return StreamingResponse(
                iter([doc_bytes]),
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={
                    "Content-Disposition": f"attachment; filename=PDD_{body.process_name.replace(' ', '_')}.docx"
                }
            )

        elif body.format == 'pdf':
            # For PDF, we return HTML that can be printed to PDF
            # This is a workaround since true PDF generation requires additional libraries
            html_content = export_service.create_html_document(
                body.process_name,
                body.sections,
                body.diagram_code
            )

            return HTMLResponse(
                content=html_content,
                headers={
                    "Content-Disposition": f"inline; filename=PDD_{body.process_name.replace(' ', '_')}.html"
                }
            )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported format: {body.format}. Supported: html, docx, pdf"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export document: {str(e)}"
        )
