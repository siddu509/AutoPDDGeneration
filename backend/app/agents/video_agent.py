"""
Video processing agent for extracting process information from screen recordings.
This agent transcribes audio, analyzes video frames, and synthesizes the information.
"""

import os
import tempfile
import subprocess
from typing import List, Tuple
from base64 import b64encode
from pathlib import Path

from openai import OpenAI
from langchain_openai import ChatOpenAI


# Initialize OpenAI client
client = OpenAI()


def transcribe_audio_from_video(video_path: str) -> str:
    """
    Extract audio from video and transcribe it using OpenAI Whisper API.

    Args:
        video_path: Path to the video file

    Returns:
        Transcribed text from the video audio

    Raises:
        Exception: If audio extraction or transcription fails
    """
    temp_audio_path = None
    try:
        # Create temporary file for audio
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
            temp_audio_path = temp_audio.name

        # Extract audio using ffmpeg
        subprocess.run(
            ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame', '-q:a', '2', temp_audio_path, '-y'],
            check=True,
            capture_output=True
        )

        # Transcribe using OpenAI Whisper API
        with open(temp_audio_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )

        return transcription

    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg error: {e.stderr.decode('utf-8')}")
    except Exception as e:
        raise Exception(f"Error transcribing audio: {str(e)}")
    finally:
        # Clean up temporary audio file
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.unlink(temp_audio_path)
            except Exception:
                pass


def analyze_video_frames(video_path: str, transcript: str) -> str:
    """
    Extract frames from video and analyze them using GPT-4o vision model.

    Args:
        video_path: Path to the video file
        transcript: Audio transcript from the video

    Returns:
        Chronological list of visual actions detected in the video

    Raises:
        Exception: If frame extraction or analysis fails
    """
    temp_frame_dir = None
    frame_paths = []

    try:
        # Create temporary directory for frames
        temp_frame_dir = tempfile.mkdtemp()

        # Extract frames using ffmpeg (1 frame every 3 seconds)
        subprocess.run(
            [
                'ffmpeg', '-i', video_path,
                '-vf', 'fps=1/3',
                f'{temp_frame_dir}/frame_%04d.jpg',
                '-y'
            ],
            check=True,
            capture_output=True
        )

        # Get list of extracted frames
        frame_paths = sorted(Path(temp_frame_dir).glob('frame_*.jpg'))

        if not frame_paths:
            raise Exception("No frames were extracted from the video")

        # Initialize vision model
        vision_model = ChatOpenAI(model="gpt-4o", temperature=0)

        # Analyze each frame
        visual_actions = []

        for i, frame_path in enumerate(frame_paths):
            try:
                # Read image and encode to base64
                with open(frame_path, 'rb') as image_file:
                    image_data = b64encode(image_file.read()).decode('utf-8')

                # Create vision prompt
                vision_prompt = f"""
You are an expert RPA analyst analyzing a screen recording.
The transcript of the video is: '{transcript}'

Analyze this screenshot (frame {i+1} of {len(frame_paths)}) and describe the specific UI action being performed at this moment.
Focus on:
- What is being clicked?
- What data is being typed?
- What is being selected?
- What screen or application is visible?

Be concise and descriptive (2-3 sentences max).
"""

                # Call vision model with image
                from langchain_core.messages import HumanMessage
                message = HumanMessage(
                    content=[
                        {"type": "text", "text": vision_prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                        }
                    ]
                )

                response = vision_model.invoke([message])
                frame_description = response.content.strip()

                visual_actions.append(f"Frame {i+1}: {frame_description}")

            except Exception as e:
                print(f"Warning: Failed to analyze frame {i+1}: {str(e)}")
                continue

        return '\n\n'.join(visual_actions)

    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg error extracting frames: {e.stderr.decode('utf-8')}")
    except Exception as e:
        raise Exception(f"Error analyzing video frames: {str(e)}")
    finally:
        # Clean up temporary frames
        if temp_frame_dir and os.path.exists(temp_frame_dir):
            try:
                import shutil
                shutil.rmtree(temp_frame_dir)
            except Exception:
                pass


def synthesize_video_analysis(transcript: str, visual_actions: str) -> str:
    """
    Combine transcript and visual actions into a coherent step-by-step guide.

    Args:
        transcript: Audio transcript from the video
        visual_actions: Visual analysis of video frames

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
You are an expert UiPath Business Analyst. Your task is to create a detailed, step-by-step text guide from a screen recording analysis.

You have two sources of information:
1. The audio transcript: {transcript}

2. The visual analysis of actions: {visual_actions}

Combine these two sources to produce a single, clear, and accurate numbered list of steps for the process.
- Resolve any discrepancies between the audio and visual information
- Use the visual information to capture specific UI actions (clicks, typing, selections)
- Use the audio transcript to understand context and business logic
- The output should be a detailed guide that can be used to build a PDD

Output ONLY the step-by-step guide, nothing else.
"""

        # Generate synthesis
        response = llm.invoke(synthesis_prompt)
        return response.content.strip()

    except Exception as e:
        raise Exception(f"Error synthesizing video analysis: {str(e)}")
