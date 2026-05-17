import struct
import wave
import pytest
from pathlib import Path
from say_e11.audio import write_wav, SAMPLE_RATE, CHANNELS


def test_write_wav_creates_valid_file(tmp_path):
    pcm = b"\x00\x00" * SAMPLE_RATE  # 1 second of silence
    out = tmp_path / "out.wav"
    write_wav(pcm, out)
    with wave.open(str(out)) as wf:
        assert wf.getnchannels() == CHANNELS
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == SAMPLE_RATE
        assert wf.getnframes() == SAMPLE_RATE


def test_write_wav_preserves_content(tmp_path):
    values = [0, 100, -100, 32767, -32768]
    pcm = struct.pack(f"<{len(values)}h", *values)
    out = tmp_path / "out.wav"
    write_wav(pcm, out)
    with wave.open(str(out)) as wf:
        raw = wf.readframes(wf.getnframes())
    recovered = list(struct.unpack(f"<{len(values)}h", raw))
    assert recovered == values


def test_write_wav_accepts_path_object(tmp_path):
    pcm = b"\x00\x00" * 10
    write_wav(pcm, tmp_path / "out.wav")
    assert (tmp_path / "out.wav").exists()


def test_write_wav_accepts_string_path(tmp_path):
    pcm = b"\x00\x00" * 10
    write_wav(pcm, str(tmp_path / "out.wav"))
    assert (tmp_path / "out.wav").exists()
