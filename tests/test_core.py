import pytest
import shutil
import subprocess

from pathlib import Path
from pydub.generators import Sine

from src.voicegram.core import VoiceConverter

vc = VoiceConverter()

pytestmark = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg not found")


def _generate_wav(path: Path, duration_ms: int = 1000) -> None:
    """Generate a 1kHz sine‑wave WAV for testing."""

    tone = Sine(1000).to_audio_segment(duration=duration_ms)
    tone.export(path, format="wav")


@pytest.fixture()
def sample_audio(tmp_path: Path) -> Path:
    wav = tmp_path / "sample.wav"
    _generate_wav(wav)
    return wav


def test_mp3_to_opus(sample_audio: Path, tmp_path: Path):
    mp3 = tmp_path / "sample.mp3"
    opus = tmp_path / "sample.ogg"

    # first convert wav → mp3 using ffmpeg directly (setup step)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(sample_audio), "-c:a", "libmp3lame", str(mp3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ok = vc.mp3_to_opus(mp3, opus)
    assert ok is True
    assert opus.exists() and opus.stat().st_size > 0


def test_opus_to_mp3(sample_audio: Path, tmp_path: Path):
    opus = tmp_path / "sample.ogg"
    mp3 = tmp_path / "sample.mp3"

    # prep: wav → opus
    subprocess.run([
        "ffmpeg", "-y", "-i", str(sample_audio), "-c:a", "libopus", str(opus)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ok = vc.opus_to_mp3(opus, mp3)
    assert ok is True
    assert mp3.exists() and mp3.stat().st_size > 0
