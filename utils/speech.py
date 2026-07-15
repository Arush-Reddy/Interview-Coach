import os
import tempfile
import wave
from functools import lru_cache

import imageio_ffmpeg
import whisper


@lru_cache(maxsize=1)
def _load_whisper_model():
    """Load Whisper once; the base model downloads the first time it is used."""
    ffmpeg_folder = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
    os.environ["PATH"] = f"{ffmpeg_folder}{os.pathsep}{os.environ.get('PATH', '')}"
    return whisper.load_model("base")


def _get_wav_duration(file_path):
    try:
        with wave.open(file_path, "rb") as audio_file:
            return audio_file.getnframes() / audio_file.getframerate()
    except (wave.Error, ZeroDivisionError):
        return None


def transcribe_audio(audio_file):
    """Convert Streamlit's recorded WAV audio into text with Whisper."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temporary_file:
        temporary_file.write(audio_file.getvalue())
        temporary_path = temporary_file.name

    try:
        duration_seconds = _get_wav_duration(temporary_path)
        result = _load_whisper_model().transcribe(temporary_path, fp16=False)
        transcript = result.get("text", "").strip()

        if not transcript:
            raise ValueError("Whisper could not detect speech in this recording.")

        return transcript, duration_seconds
    finally:
        os.remove(temporary_path)
