"""
Video processing agent for extracting process information from screen recordings.
This agent transcribes audio directly from video files using OpenAI Whisper API.
"""

import os
from openai import OpenAI
from langchain_openai import ChatOpenAI


# Initialize OpenAI client
client = OpenAI()


def transcribe_audio_from_video(video_path: str) -> str:
    """
    Transcribe audio directly from video using OpenAI Whisper API.
    Note: Whisper API supports video files (mp4, mov, etc.) directly!

    Args:
        video_path: Path to the video file

    Returns:
        Transcribed text from the video audio

    Raises:
        Exception: If transcription fails
    """
    try:
        # Open and transcribe the video file directly
        # Whisper API supports: mp3, mp4, mpeg, mpga, m4a, wav, webm
        with open(video_path, 'rb') as video_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=video_file,
                response_format="text"
            )

        return transcription

    except Exception as e:
        raise Exception(f"Error transcribing video: {str(e)}")


def analyze_video_frames(video_path: str, transcript: str) -> str:
    """
    Placeholder for frame analysis (requires ffmpeg).
    Returns a message indicating frame analysis is skipped.

    Args:
        video_path: Path to the video file
        transcript: Audio transcript from the video

    Returns:
        Message about skipped frame analysis
    """
    return "Note: Visual frame analysis requires ffmpeg. Using audio transcription only."


def synthesize_video_analysis(transcript: str, visual_actions: str) -> str:
    """
    Combine transcript into a coherent step-by-step guide.

    Args:
        transcript: Audio transcript from the video
        visual_actions: Visual analysis of video frames (or note about skipping)

    Returns:
        Synthesized step-by-step process guide

    Raises:
        Exception: If synthesis fails
    """
    try:
        # Initialize LLM
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        # Create synthesis prompt
        synthesis_prompt = f"""
You are an expert UiPath Business Analyst. Your task is to create a detailed, step-by-step text guide from a screen recording.

You have the audio transcript from the video:
{transcript}

Visual analysis note: {visual_actions}

Based on the audio transcript, create a comprehensive, numbered list of steps that describes the process in detail.
- Focus on specific actions, inputs, and decisions mentioned in the audio
- Include any specific field names, button names, or navigation steps described
- Organize into clear, sequential steps
- Add details about business rules or conditions mentioned

Output ONLY the step-by-step guide, nothing else.
"""

        # Generate synthesis
        response = llm.invoke(synthesis_prompt)
        return response.content.strip()

    except Exception as e:
        raise Exception(f"Error synthesizing video analysis: {str(e)}")
