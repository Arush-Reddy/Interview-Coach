import os
import shutil
import tempfile
import wave
from functools import lru_cache
from pathlib import Path

import imageio_ffmpeg
import whisper


@lru_cache(maxsize=1)
def _configure_ffmpeg():
    """Expose imageio's versioned binary under the name Whisper invokes."""
    source = Path(imageio_ffmpeg.get_ffmpeg_exe())
    executable_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"

    if source.name.lower() == executable_name:
        executable = source
    else:
        shim_directory = Path(tempfile.gettempdir()) / "ai-interview-coach-bin"
        shim_directory.mkdir(parents=True, exist_ok=True)
        executable = shim_directory / executable_name
        if not executable.exists() or executable.stat().st_size != source.stat().st_size:
            shutil.copy2(source, executable)

    os.environ["PATH"] = (
        f"{executable.parent}{os.pathsep}{os.environ.get('PATH', '')}"
    )
    return executable


@lru_cache(maxsize=1)
def _load_whisper_model():
    """Load Whisper once; the base model downloads the first time it is used."""
    _configure_ffmpeg()
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
