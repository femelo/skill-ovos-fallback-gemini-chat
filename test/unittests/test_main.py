from __future__ import annotations
import shutil
from os import environ
from os.path import dirname, join
from threading import Event
from pyee import EventEmitter
from unittest import TestCase
from unittest.mock import MagicMock, Mock

import pytest
from ovos_utils.fakebus import FakeBus
from ovos_bus_client.message import Message
from skill_ovos_fallback_gemini_chat import (
    DEFAULT_SETTINGS, GeminiChatSkill
)


class DerivedFakeBus(FakeBus):
    def __init__(self: DerivedFakeBus) -> None:
        super().__init__()
        self.emitter: EventEmitter | None = None
        self.connected_event: Event | None = None


class TestGeminiChatSkill(TestCase):
    # Define test directories
    test_fs = join(dirname(__file__), "skill_fs")
    data_dir = join(test_fs, "data")
    conf_dir = join(test_fs, "config")
    environ["XDG_DATA_HOME"] = data_dir
    environ["XDG_CONFIG_HOME"] = conf_dir

    bus = DerivedFakeBus()
    bus.emitter = bus.ee
    bus.connected_event = Event()
    bus.connected_event.set()
    bus.run_forever()
    test_skill_id = 'test_skill.test'

    skill: GeminiChatSkill | None = None

    @classmethod
    def setup_class(cls) -> None:
        # Get test skill
        cls.skill = GeminiChatSkill(skill_id=cls.test_skill_id, bus=cls.bus)
        # Override speak and speak_dialog to test passed arguments
        cls.skill.speak = Mock()
        cls.skill.speak_dialog = Mock()

    def setup(self: TestGeminiChatSkill) -> None:
        if not self.skill:
            raise ValueError("Skill not initialized")
        if isinstance(self.skill.speak, Mock):
            self.skill.speak.reset_mock()
        if isinstance(self.skill.speak_dialog, Mock):
            self.skill.speak_dialog.reset_mock()
        self.skill.play_audio = Mock()
        self.skill.log = MagicMock()

    @classmethod
    def tear_down_class(cls) -> None:
        shutil.rmtree(cls.test_fs)

    def test_default_no_key(self: TestGeminiChatSkill) -> None:
        assert self.skill is not None
        assert not self.skill.settings.get("key")
        message = Message("test", {"utterance": "Will my test pass?"})
        self.skill.ask_gemini_chat(message)
        assert isinstance(self.skill.log, MagicMock)
        self.skill.log.error.assert_called()
        assert isinstance(self.skill.speak_dialog, Mock)
        self.skill.speak_dialog.assert_not_called()  # no key, we log an error before speaking ever happens
        assert self.skill.settings.get("persona") == DEFAULT_SETTINGS["persona"]
        assert self.skill.settings.get("model") == DEFAULT_SETTINGS["model"]

    def test_default_with_key(self: TestGeminiChatSkill) -> None:
        assert self.skill is not None
        self.skill.settings["key"] = "test"
        self.skill.settings.store()
        assert self.skill.settings.get("key") == "test"
        assert self.skill.settings.get("persona") == DEFAULT_SETTINGS["persona"]
        assert self.skill.settings.get("model") == DEFAULT_SETTINGS["model"]

    def test_overriding_all_settings(self: TestGeminiChatSkill) -> None:
        assert self.skill is not None
        self.skill.settings["key"] = "test"
        self.skill.settings["persona"] = "I am a test persona"
        self.skill.settings["model"] = "gpt-4-nitro"
        self.skill.settings.store()
        assert self.skill.settings.get("key") == "test"
        assert self.skill.settings.get("persona") == "I am a test persona"
        assert self.skill.settings.get("model") == "gpt-4-nitro"
        assert self.skill.settings.get("persona") != DEFAULT_SETTINGS["persona"]
        assert self.skill.settings.get("model") != DEFAULT_SETTINGS["model"]


if __name__ == "__main__":
    pytest.main()
