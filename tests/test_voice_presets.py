from say_e11.providers.elevenlabs import VOICE_PRESETS, DEFAULT_VOICE, resolve_voice


def test_presets_has_10_voices():
    assert len(VOICE_PRESETS) == 10


def test_resolve_none_returns_default():
    assert resolve_voice(None) == DEFAULT_VOICE


def test_resolve_known_preset_by_name():
    assert resolve_voice("rachel") == "21m00Tcm4TlvDq8ikWAM"
    assert resolve_voice("bella") == "EXAVITQu4vr4xnSDxMaL"


def test_resolve_preset_case_insensitive():
    assert resolve_voice("RACHEL") == resolve_voice("rachel")
    assert resolve_voice("Bella") == resolve_voice("bella")


def test_resolve_raw_id_passthrough():
    raw_id = "customVoiceId123"
    assert resolve_voice(raw_id) == raw_id


def test_all_preset_ids_are_nonempty():
    for name, vid in VOICE_PRESETS.items():
        assert vid, f"voice '{name}' has an empty ID"
