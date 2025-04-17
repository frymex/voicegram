from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from typing import Any, Final

from .core import VoiceConverter

try:
    __version__: Final[str] = version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.1.dev0"

__all__ = [
    "VoiceConverter",
    "mp3_to_opus",
    "opus_to_mp3",
    "__version__",
]

_default = VoiceConverter()

def mp3_to_opus(*args: Any, **kwds: Any) -> bool:
    return _default.mp3_to_opus(*args, **kwds)

def opus_to_mp3(*args: Any, **kwds: Any) -> bool:
    return _default.opus_to_mp3(*args, **kwds)
