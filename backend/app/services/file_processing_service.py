"""
File Processing Service for handling uploaded files.

This service manages the processing of uploaded files (PDF, DOCX, MP4, etc.),
including temporary file management and routing to appropriate processors.
"""

import os
import tempfile
from pathlib import Path
from typing import Tuple, Optional

from app.utils.file_parser import parse_document
from app.agents.video_agent import (
    transcribe_audio_from_video,
    analyze_video_frames,
    synthesize_video_analysis
)
from app.core.config import get_logger

# Get module logger
logger = get_logger(__name__)


class FileProcessingService:
    """
    Service for processing uploaded files.

    This service handles file upload processing workflow:
    1. Save uploaded file to temporary location
    2. Determine file type
    3. Route to appropriate processor (document or video)
    4. Clean up temporary file

    Attributes:
        temp_file_path: Path to current temporary file (if any)

    Example:
        >>> service = FileProcessingService()
        >>> text, ext = await service.process_upload(
        ...     file_content,
        ...     "document.pdf"
        ... )
        >>> service.cleanup()  # Always call when done
    """

    SUPPORTED_DOC = ['.pdf', '.docx']
    SUPPORTED_VIDEO = ['.mp4', '.mov', '.avi']

    def __init__(self):
        """Initialize FileProcessingService."""
        self.temp_file_path: Optional[str] = None

    async def process_upload(self, file_content: bytes, filename: str) -> Tuple[str, str]:
        """
        Process uploaded file and extract text.

        This method orchestrates the entire file processing workflow:
        - Saves uploaded content to temporary file
        - Determines file type from extension
        - Routes to appropriate processor
        - Returns extracted text and file type

        Args:
            file_content: Raw file content as bytes
            filename: Original filename with extension

        Returns:
            Tuple of (extracted_text, file_extension)

        Raises:
            ValueError: If file type is not supported

        Example:
            >>> service = FileProcessingService()
            >>> with open("document.pdf", "rb") as f:
            ...     content = f.read()
            >>> text, ext = await service.process_upload(
            ...     content,
            ...     "document.pdf"
            ... )
            >>> print(f"Extracted {len(text)} characters from {ext} file")
        """
        # Save to temp file
        self.temp_file_path = self._save_temp_file(file_content, filename)

        # Get extension
        file_extension = Path(filename).suffix.lower()

        # Process based on type
        if file_extension in self.SUPPORTED_DOC:
            text = parse_document(self.temp_file_path)
        elif file_extension in self.SUPPORTED_VIDEO:
            text = self._process_video(self.temp_file_path)
        else:
            raise ValueError(
                f"Unsupported file type: {file_extension}. "
                f"Supported types: {', '.join(self.SUPPORTED_DOC + self.SUPPORTED_VIDEO)}"
            )

        return text, file_extension

    def _process_video(self, video_path: str) -> str:
        """
        Process video file: transcribe audio and analyze.

        Processes video files through the video analysis pipeline:
        1. Transcribe audio using Whisper API
        2. Analyze video frames (placeholder, requires ffmpeg)
        3. Synthesize into step-by-step guide

        Args:
            video_path: Path to video file

        Returns:
            Synthesized process description from video

        Example:
            >>> service = FileProcessingService()
            >>> text = service._process_video("/path/to/video.mp4")
            >>> print(text)
            'Step 1: Open the application...'
        """
        transcript = transcribe_audio_from_video(video_path)
        visual_actions = analyze_video_frames(video_path, transcript)
        return synthesize_video_analysis(transcript, visual_actions)

    def _save_temp_file(self, content: bytes, filename: str) -> str:
        """
        Save content to temporary file.

        Creates a temporary file with a unique name that includes
        the original filename for debugging purposes.

        Args:
            content: File content as bytes
            filename: Original filename (used for temp file suffix)

        Returns:
            Path to temporary file

        Example:
            >>> service = FileProcessingService()
            >>> path = service._save_temp_file(
            ...     b"file content",
            ...     "document.pdf"
            ... )
            >>> print(path)
            '/tmp/tmpXXXXXX_document.pdf'
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as temp_file:
            temp_file.write(content)
            self.temp_file_path = temp_file.name
        return self.temp_file_path

    def cleanup(self):
        """
        Clean up temporary file.

        Should always be called after processing is complete to prevent
        disk space issues. Uses try-except to ensure cleanup doesn't
        raise exceptions.

        Example:
            >>> service = FileProcessingService()
            >>> try:
            ...     text = await service.process_upload(content, filename)
            ... finally:
            ...     service.cleanup()  # Ensure cleanup runs
        """
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            try:
                os.unlink(self.temp_file_path)
            except Exception as e:
                logger.warning(
                    f"Failed to cleanup temp file {self.temp_file_path}: {e}"
                )
