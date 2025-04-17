# voicegram

> Lightweight Python **library** that converts any audio file into a Telegram‑ready voice note (OGG/Opus) — and back again.

[![PyPI](https://img.shields.io/pypi/v/voicegram.svg)](https://pypi.org/project/voicegram/)
[![CI](https://github.com/frymex/voicegram/actions/workflows/ci.yml/badge.svg)](https://github.com/frymex/voicegram/actions)

---

## Why?

Telegram expects voice messages in a fairly specific format: Opus‑encoded OGG, 48 kHz, mono/stereo. Configuring `ffmpeg` every time is tedious. **voicegram** wraps those flags in a minimal API, so your code can simply read:

```python
from voicegram import VoiceConverter, mp3_to_opus

vc = VoiceConverter()
vc.mp3_to_opus("song.mp3", "note.ogg")  # library call

# or one‑liner helper
mp3_to_opus("song.mp3")                   # -> song.ogg
```

No boilerplate, no codec guessing.

---

## Installation

```bash
pip install voicegram  # Python ≥ 3.9 and ffmpeg ≥ 4.3 required
```

---

## Quick start

```python
from voicegram import VoiceConverter

vc = VoiceConverter()

# Convert anything ffmpeg can read to Telegram voice note
vc.mp3_to_opus("voice.wav")          # → voice.ogg

# Convert it back to MP3 (e.g. for sharing elsewhere)
vc.opus_to_mp3("voice.ogg")          # → voice.mp3
```

---

## API reference

| Method | Purpose |
|--------|---------|
| `VoiceConverter.mp3_to_opus(src, dst=None, bitrate="96k", vbr=True)` | Convert arbitrary audio to Opus‑encoded OGG. |
| `VoiceConverter.opus_to_mp3(src, dst=None, quality="2")` | Convert OGG/Opus back to MP3. |

Additionally, top‑level helpers `mp3_to_opus()` and `opus_to_mp3()` proxy to a shared converter instance.

Full docs live in the [wiki](https://github.com/frymex/voicegram/wiki).

---

## Development

```bash
git clone https://github.com/frymex/voicegram
cd voicegram
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]      # pytest, black, mypy, pre‑commit …
pytest -q
```

### Releasing

1. Bump version in `pyproject.toml`.
2. `git tag vX.Y.Z && git push --tags`.
3. GitHub Actions publishes wheels to PyPI via Trusted Publisher.

---

## License

MIT — see [LICENSE](LICENSE) for details.
