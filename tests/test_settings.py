import json
import pytest
from pathlib import Path
from unittest.mock import patch
from say_e11.settings import load, save_key


@pytest.fixture()
def config_file(tmp_path):
    cfg = tmp_path / "config.json"
    config_dir = tmp_path
    with (
        patch("say_e11.settings._CONFIG_DIR", config_dir),
        patch("say_e11.settings._CONFIG_FILE", cfg),
    ):
        yield cfg


def test_load_returns_empty_when_no_file(config_file):
    assert load() == {}


def test_save_and_load_voice(config_file):
    save_key("voice", "bella")
    assert load()["voice"] == "bella"


def test_save_and_load_rate(config_file):
    save_key("rate", "200")
    assert load()["rate"] == 200


def test_save_and_load_provider(config_file):
    save_key("provider", "deepgram")
    assert load()["provider"] == "deepgram"


def test_save_invalid_key_exits(config_file):
    with pytest.raises(SystemExit):
        save_key("model", "gpt4")


def test_save_invalid_provider_exits(config_file):
    with pytest.raises(SystemExit):
        save_key("provider", "openai")


def test_save_invalid_rate_exits(config_file):
    with pytest.raises(SystemExit):
        save_key("rate", "fast")


def test_save_overwrites_existing(config_file):
    save_key("voice", "rachel")
    save_key("voice", "bella")
    assert load()["voice"] == "bella"


def test_load_handles_corrupt_file(config_file):
    config_file.write_text("not json", encoding="utf-8")
    assert load() == {}
