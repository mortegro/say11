import wave
from pathlib import Path

import numpy as np
import sounddevice as sd

SAMPLE_RATE = 24_000
CHANNELS = 1


def play_pcm(pcm: bytes) -> None:
    if len(pcm) % 2 != 0:
        raise ValueError(f"PCM length {len(pcm)} is not a multiple of 2 (truncated data?)")
    audio = np.frombuffer(pcm, dtype=np.int16)
    sd.play(audio, samplerate=SAMPLE_RATE)
    sd.wait()


def write_wav(pcm: bytes, path: str | Path) -> None:
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit = 2 bytes per sample
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm)
