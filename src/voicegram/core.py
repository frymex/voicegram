from __future__ import annotations

"""voicegram.core
~~~~~~~~~~~~~~~~~~
Core conversion utilities for the *voicegram* package.

This module defines :class:`VoiceConverter`, a lightweight wrapper
around *ffmpeg* that can convert

* generic audio (e.g. MP3, WAV, FLAC) → OGG/Opus suitable for Telegram
  voice messages,
* OGG/Opus → MP3 for wider compatibility.

Example
=======
>>> from voicegram.core import VoiceConverter
>>> vc = VoiceConverter()
>>> vc.mp3_to_opus("song.mp3", "note.ogg")
True
"""

from pathlib import Path
import subprocess
from typing import Sequence, Union

__all__ = [
    "VoiceConverter",
]

PathLike = Union[str, Path]


class VoiceConverter:
    """А thin *ffmpeg* façade for audio ↔ Telegram‑voice conversions.

    Parameters
    ----------
    ffmpeg_binary:
        Executable to invoke. Defaults to the plain ``"ffmpeg"`` that
        should be resolvable via ``PATH``. Override if you bundle or
        vend a custom build.
    """

    def __init__(self, ffmpeg_binary: str = "ffmpeg") -> None:
        self.ffmpeg: str = ffmpeg_binary

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def mp3_to_opus(
            self,
            input_path: PathLike,
            output_path: PathLike | None = None,
            *,
            bitrate: str = "96k",
            vbr: bool = True,
    ) -> bool:
        """Convert *any* audio file (not just MP3) to OGG/Opus.

        By default Telegram expects:
        * mono or stereo, 48 kHz,
        * libopus‐encoded OGG.
        """

        input_p = Path(input_path)
        output_p = Path(output_path) if output_path else input_p.with_suffix(".ogg")

        cmd: list[str] = [
            self.ffmpeg,
            "-i",
            str(input_p),
            "-c:a",
            "libopus",
        ]
        if vbr:
            cmd.extend(["-vbr", "on"])
        cmd.extend(["-b:a", bitrate, "-vn", "-y", str(output_p)])

        return self._run(cmd)

    def opus_to_mp3(
            self,
            input_path: PathLike,
            output_path: PathLike | None = None,
            *,
            quality: str = "2",
    ) -> bool:
        """Convert OGG/Opus back to MP3.

        Parameters
        ----------
        quality:
            LAME VBR quality (``0``–``9``). ``2`` ≈~192kbps and is
            usually transparent.
        """

        input_p = Path(input_path)
        output_p = Path(output_path) if output_path else input_p.with_suffix(".mp3")

        cmd: list[str] = [
            self.ffmpeg,
            "-i",
            str(input_p),
            "-c:a",
            "libmp3lame",
            "-q:a",
            quality,
            "-vn",
            "-y",
            str(output_p),
        ]

        return self._run(cmd)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    @staticmethod
    def _run(cmd: Sequence[str]) -> bool:
        """Execute *ffmpeg* command; return *True* on non‑error exit."""

        try:
            subprocess.run(cmd, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
