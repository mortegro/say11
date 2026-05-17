import os
import pytest
from pathlib import Path
from unittest.mock import patch
from say_e11.config import load_env, pick_provider


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    monkeypatch.delenv("DEEPGRAM_API_KEY", raising=False)


# --- load_env tests ---

def test_load_env_sets_key_from_local_env(tmp_path, monkeypatch):
    (tmp_path / ".env").write_text("ELEVENLABS_API_KEY=from-local\n")
    load_env(local_env=tmp_path / ".env")
    assert os.environ.get("ELEVENLABS_API_KEY") == "from-local"


def test_load_env_local_wins_over_home(tmp_path, monkeypatch):
    home_env = tmp_path / "home.env"
    home_env.write_text("ELEVENLABS_API_KEY=from-home\n")
    local_env = tmp_path / "local.env"
    local_env.write_text("ELEVENLABS_API_KEY=from-local\n")
    load_env(home_env=home_env, local_env=local_env)
    assert os.environ.get("ELEVENLABS_API_KEY") == "from-local"


def test_load_env_home_used_when_no_local(tmp_path, monkeypatch):
    home_env = tmp_path / "home.env"
    home_env.write_text("DEEPGRAM_API_KEY=from-home\n")
    load_env(home_env=home_env, local_env=tmp_path / "nonexistent.env")
    assert os.environ.get("DEEPGRAM_API_KEY") == "from-home"


def test_load_env_does_not_override_process_env(tmp_path, monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "process-value")
    local_env = tmp_path / ".env"
    local_env.write_text("ELEVENLABS_API_KEY=from-file\n")
    load_env(local_env=local_env)
    assert os.environ.get("ELEVENLABS_API_KEY") == "process-value"


# --- pick_provider tests ---

def test_pick_provider_prefers_elevenlabs_when_both_present(monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "el-key")
    monkeypatch.setenv("DEEPGRAM_API_KEY", "dg-key")
    with patch("say_e11.config.load_env"):
        name, key, source = pick_provider(None)
    assert name == "elevenlabs"
    assert key == "el-key"
    assert source == "process environment"


def test_pick_provider_falls_back_to_deepgram(monkeypatch):
    monkeypatch.setenv("DEEPGRAM_API_KEY", "dg-key")
    with patch("say_e11.config.load_env"):
        name, key, source = pick_provider(None)
    assert name == "deepgram"
    assert key == "dg-key"
    assert source == "process environment"


def test_pick_provider_forced_deepgram(monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "el-key")
    monkeypatch.setenv("DEEPGRAM_API_KEY", "dg-key")
    with patch("say_e11.config.load_env"):
        name, key, source = pick_provider("deepgram")
    assert name == "deepgram"
    assert key == "dg-key"
    assert source == "process environment"


def test_pick_provider_forced_elevenlabs(monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "el-key")
    with patch("say_e11.config.load_env"):
        name, key, source = pick_provider("elevenlabs")
    assert name == "elevenlabs"
    assert key == "el-key"
    assert source == "process environment"


def test_pick_provider_source_from_local_env(monkeypatch):
    # Simulate key only in local .env (not process env, not home .env)
    with patch("say_e11.config.dotenv_values") as mock_dv:
        mock_dv.side_effect = lambda p: (
            {"ELEVENLABS_API_KEY": "from-local"} if Path(p).parent != Path.home() else {}
        )
        # load_env is NOT mocked so it applies the value from mocked dotenv_values
        name, key, source = pick_provider(None)
    assert name == "elevenlabs"
    assert key == "from-local"
    assert source == "./.env"


def test_pick_provider_source_from_home_env(monkeypatch):
    # Simulate key only in ~/.env
    with patch("say_e11.config.dotenv_values") as mock_dv:
        mock_dv.side_effect = lambda p: (
            {"ELEVENLABS_API_KEY": "from-home"} if Path(p).parent == Path.home() else {}
        )
        name, key, source = pick_provider(None)
    assert source == "~/.env"


def test_pick_provider_no_key_exits(monkeypatch):
    with patch("say_e11.config.load_env"):
        with pytest.raises(SystemExit):
            pick_provider(None)


def test_pick_provider_forced_missing_key_exits(monkeypatch):
    with patch("say_e11.config.load_env"):
        with pytest.raises(SystemExit):
            pick_provider("elevenlabs")
