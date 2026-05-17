import io
import struct
import wave
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from say_e11.cli import main

FAKE_PCM = struct.pack("<4h", 0, 100, -100, 200)


def make_provider(pcm: bytes = FAKE_PCM) -> MagicMock:
    p = MagicMock()
    p.synthesize.return_value = pcm
    p.__enter__.return_value = p
    p.__exit__.return_value = None
    return p


@pytest.fixture(autouse=True)
def no_audio(monkeypatch):
    monkeypatch.setattr("say_e11.cli.play_pcm", lambda pcm: None)


@pytest.fixture(autouse=True)
def no_settings(monkeypatch):
    monkeypatch.setattr("say_e11.cli.load_settings", lambda: {})


def test_text_from_positional_args(monkeypatch):
    provider = make_provider()
    monkeypatch.setattr("sys.argv", ["say", "hello", "world"])
    with patch("say_e11.cli.pick_provider", return_value=("elevenlabs", "key", "process environment")):
        with patch("say_e11.cli.build_provider", return_value=provider):
            main()
    provider.synthesize.assert_called_once_with("hello world", None, 175)


def test_text_from_stdin(monkeypatch):
    provider = make_provider()
    monkeypatch.setattr("sys.argv", ["say"])
    monkeypatch.setattr("sys.stdin", io.StringIO("piped text"))
    with patch("say_e11.cli.pick_provider", return_value=("elevenlabs", "key", "process environment")):
        with patch("say_e11.cli.build_provider", return_value=provider):
            main()
    provider.synthesize.assert_called_once_with("piped text", None, 175)


def test_text_from_file(monkeypatch, tmp_path):
    provider = make_provider()
    f = tmp_path / "text.txt"
    f.write_text("file content")
    monkeypatch.setattr("sys.argv", ["say", "-f", str(f)])
    with patch("say_e11.cli.pick_provider", return_value=("elevenlabs", "key", "process environment")):
        with patch("say_e11.cli.build_provider", return_value=provider):
            main()
    provider.synthesize.assert_called_once_with("file content", None, 175)


def test_output_writes_wav(monkeypatch, tmp_path):
    provider = make_provider()
    out = tmp_path / "out.wav"
    monkeypatch.setattr("sys.argv", ["say", "-o", str(out), "hello"])
    with patch("say_e11.cli.pick_provider", return_value=("elevenlabs", "key", "process environment")):
        with patch("say_e11.cli.build_provider", return_value=provider):
            main()
    assert out.exists()
    with wave.open(str(out)) as wf:
        assert wf.getnchannels() == 1
        assert wf.getframerate() == 24000


def test_voice_and_rate_passed_through(monkeypatch):
    provider = make_provider()
    monkeypatch.setattr("sys.argv", ["say", "-V", "my-voice", "-R", "200", "hello"])
    with patch("say_e11.cli.pick_provider", return_value=("elevenlabs", "key", "process environment")):
        with patch("say_e11.cli.build_provider", return_value=provider):
            main()
    provider.synthesize.assert_called_once_with("hello", "my-voice", 200)


def test_provider_flag_forwarded(monkeypatch):
    provider = make_provider()
    monkeypatch.setattr("sys.argv", ["say", "--provider", "deepgram", "hello"])
    with patch("say_e11.cli.pick_provider", return_value=("deepgram", "key", "process environment")) as mock_pick:
        with patch("say_e11.cli.build_provider", return_value=provider):
            main()
    mock_pick.assert_called_once_with("deepgram")


def test_provider_error_exits(monkeypatch):
    provider = make_provider()
    provider.synthesize.side_effect = RuntimeError("API error")
    monkeypatch.setattr("sys.argv", ["say", "hello"])
    with patch("say_e11.cli.pick_provider", return_value=("elevenlabs", "key", "process environment")):
        with patch("say_e11.cli.build_provider", return_value=provider):
            with pytest.raises(SystemExit):
                main()


def test_no_text_no_args_exits(monkeypatch):
    class FakeTTY(io.StringIO):
        def isatty(self) -> bool:
            return True

    monkeypatch.setattr("sys.argv", ["say"])
    monkeypatch.setattr("sys.stdin", FakeTTY())
    with pytest.raises(SystemExit):
        main()


def test_empty_text_exits(monkeypatch):
    monkeypatch.setattr("sys.argv", ["say", "   "])
    with pytest.raises(SystemExit):
        main()


def test_missing_file_exits(monkeypatch, tmp_path):
    monkeypatch.setattr("sys.argv", ["say", "-f", str(tmp_path / "missing.txt")])
    with pytest.raises(SystemExit):
        main()


def test_list_voices_prints_presets(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["say", "--list-voices"])
    main()
    out = capsys.readouterr().out
    assert "rachel" in out
    assert "bella" in out
    assert "21m00Tcm4TlvDq8ikWAM" in out


def test_show_config_empty(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["say", "--show-config"])
    main()
    assert "No defaults" in capsys.readouterr().out


def test_show_config_with_settings(monkeypatch, capsys):
    monkeypatch.setattr("say_e11.cli.load_settings", lambda: {"voice": "bella", "rate": 200})
    monkeypatch.setattr("sys.argv", ["say", "--show-config"])
    main()
    out = capsys.readouterr().out
    assert "voice" in out
    assert "bella" in out


def test_set_saves_to_config(monkeypatch):
    monkeypatch.setattr("sys.argv", ["say", "--set", "voice", "rachel"])
    with patch("say_e11.cli.save_key") as mock_save:
        main()
    mock_save.assert_called_once_with("voice", "rachel")


def test_settings_voice_used_as_default(monkeypatch):
    monkeypatch.setattr("say_e11.cli.load_settings", lambda: {"voice": "bella"})
    provider = make_provider()
    monkeypatch.setattr("sys.argv", ["say", "hello"])
    with patch("say_e11.cli.pick_provider", return_value=("elevenlabs", "key", "process environment")):
        with patch("say_e11.cli.build_provider", return_value=provider):
            main()
    provider.synthesize.assert_called_once_with("hello", "bella", 175)


def test_cli_voice_overrides_settings(monkeypatch):
    monkeypatch.setattr("say_e11.cli.load_settings", lambda: {"voice": "bella"})
    provider = make_provider()
    monkeypatch.setattr("sys.argv", ["say", "-V", "josh", "hello"])
    with patch("say_e11.cli.pick_provider", return_value=("elevenlabs", "key", "process environment")):
        with patch("say_e11.cli.build_provider", return_value=provider):
            main()
    provider.synthesize.assert_called_once_with("hello", "josh", 175)


def test_settings_rate_used_as_default(monkeypatch):
    monkeypatch.setattr("say_e11.cli.load_settings", lambda: {"rate": 200})
    provider = make_provider()
    monkeypatch.setattr("sys.argv", ["say", "hello"])
    with patch("say_e11.cli.pick_provider", return_value=("elevenlabs", "key", "process environment")):
        with patch("say_e11.cli.build_provider", return_value=provider):
            main()
    provider.synthesize.assert_called_once_with("hello", None, 200)


def test_verbose_prints_provider_key_source_voice(monkeypatch, capsys):
    provider = make_provider()
    monkeypatch.setattr("sys.argv", ["say", "-v", "-V", "rachel", "hello"])
    with patch("say_e11.cli.pick_provider", return_value=("elevenlabs", "key", "./.env")):
        with patch("say_e11.cli.build_provider", return_value=provider):
            main()
    err = capsys.readouterr().err
    assert "elevenlabs" in err
    assert "./.env" in err
    assert "rachel" in err


def test_verbose_default_voice_label(monkeypatch, capsys):
    provider = make_provider()
    monkeypatch.setattr("sys.argv", ["say", "-v", "hello"])
    with patch("say_e11.cli.pick_provider", return_value=("deepgram", "key", "~/.env")):
        with patch("say_e11.cli.build_provider", return_value=provider):
            main()
    err = capsys.readouterr().err
    assert "deepgram" in err
    assert "~/.env" in err
    assert "(default)" in err
