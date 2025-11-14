"""Speech-to-Text service using OpenAI Whisper"""
from typing import Optional, BinaryIO
import httpx
from app.config import settings


class STTService:
    """
    Speech-to-Text service abstraction.
    Uses OpenAI Whisper API for transcription.
    """

    @staticmethod
    async def transcribe_audio(audio_data: BinaryIO, filename: str = "audio.wav") -> str:
        """
        Transcribe audio to text.

        Args:
            audio_data: Audio file bytes
            filename: Original filename (for API)

        Returns:
            Transcribed text

        Note:
            If OPENAI_API_KEY is not set, returns a stub transcription.
            To enable real transcription, set OPENAI_API_KEY in .env
        """
        if not settings.OPENAI_API_KEY:
            # Stub implementation for development
            return "[Transcription stub - Please set OPENAI_API_KEY to enable real STT]"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                files = {
                    "file": (filename, audio_data, "audio/wav"),
                    "model": (None, "whisper-1"),
                }
                headers = {
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
                }

                response = await client.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    files=files,
                    headers=headers
                )
                response.raise_for_status()

                result = response.json()
                return result.get("text", "")

        except Exception as e:
            print(f"STT Error: {e}")
            return f"[Transcription failed: {str(e)}]"
