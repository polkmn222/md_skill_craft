"""Tests for localization module."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from md_skill_craft.config.localization import get_string, get_text, STRINGS


class TestLocalizationStrings:
    """Test localization strings."""

    def test_english_strings_exist(self):
        """Test that all strings have English translations."""
        for key, translations in STRINGS.items():
            assert "en" in translations, f"Missing English translation for {key}"
            assert isinstance(translations["en"], str), f"English translation for {key} is not a string"
            assert len(translations["en"]) > 0, f"English translation for {key} is empty"

    def test_korean_strings_exist(self):
        """Test that all strings have Korean translations."""
        for key, translations in STRINGS.items():
            assert "ko" in translations, f"Missing Korean translation for {key}"
            assert isinstance(translations["ko"], str), f"Korean translation for {key} is not a string"
            assert len(translations["ko"]) > 0, f"Korean translation for {key} is empty"

    def test_string_keys_are_unique(self):
        """Test that all string keys are unique."""
        keys = list(STRINGS.keys())
        assert len(keys) == len(set(keys)), "Duplicate keys found in STRINGS"

    def test_string_key_format(self):
        """Test that string keys follow the naming convention."""
        for key in STRINGS.keys():
            parts = key.split(".")
            assert len(parts) >= 2, f"Key '{key}' should have at least 2 parts separated by dots"


class TestGetString:
    """Test get_string function."""

    def test_get_english_string(self):
        """Test getting English string."""
        result = get_string("section.language_select", "en")
        assert result == "[1/4] Select Language"
        assert "Korean" not in result

    def test_get_korean_string(self):
        """Test getting Korean string."""
        result = get_string("section.language_select", "ko")
        assert result == "[1/4] Language 선택"
        assert "선택" in result

    def test_get_string_default_to_english(self):
        """Test that missing language defaults to English."""
        result = get_string("section.language_select", "fr")
        assert result == "[1/4] Select Language"

    def test_get_string_with_format_params(self):
        """Test get_string with format parameters."""
        result = get_string("analysis.save_as_suggested", "en", file_type="AGENT")
        assert "AGENT" in result
        assert "Save as" in result

    def test_get_string_with_format_params_korean(self):
        """Test get_string with format parameters in Korean."""
        result = get_string("analysis.save_as_suggested", "ko", file_type="AGENT")
        assert "AGENT" in result
        assert "저장" in result

    def test_get_string_missing_key(self):
        """Test getting non-existent key."""
        result = get_string("nonexistent.key", "en")
        assert "[MISSING:" in result
        assert "nonexistent.key" in result

    def test_get_string_with_multiple_params(self):
        """Test get_string with multiple format parameters."""
        result = get_string("analysis.file_saved", "en", filename="AGENT.md")
        assert "AGENT.md" in result
        assert "saved" in result


class TestGetText:
    """Test get_text function."""

    def test_get_text_english(self):
        """Test get_text with English."""
        result = get_text("section.language_select", "en")
        assert result == "[1/4] Select Language"

    def test_get_text_korean(self):
        """Test get_text with Korean."""
        result = get_text("section.language_select", "ko")
        assert result == "[1/4] Language 선택"

    def test_get_text_is_alias_for_get_string(self):
        """Test that get_text is equivalent to get_string without params."""
        key = "section.language_select"
        assert get_text(key, "en") == get_string(key, "en")
        assert get_text(key, "ko") == get_string(key, "ko")


class TestLocalizationCoverage:
    """Test that key UI strings are properly localized."""

    def test_onboarding_strings(self):
        """Test that onboarding strings are localized."""
        required_keys = [
            "section.language_select",
            "section.llm_select",
            "section.api_key",
            "prompt.select_language",
            "prompt.select_llm",
        ]
        for key in required_keys:
            assert key in STRINGS, f"Missing onboarding string: {key}"
            assert "en" in STRINGS[key]
            assert "ko" in STRINGS[key]

    def test_help_strings(self):
        """Test that help menu strings are localized."""
        required_keys = [
            "help.help_command",
            "help.setup_command",
            "help.cost_command",
            "help.mode_command",
            "help.exit_command",
        ]
        for key in required_keys:
            assert key in STRINGS, f"Missing help string: {key}"

    def test_mode_strings(self):
        """Test that mode strings are localized."""
        required_keys = [
            "mode.generate_guide",
            "mode.analyze_project",
        ]
        for key in required_keys:
            assert key in STRINGS, f"Missing mode string: {key}"

    def test_success_messages(self):
        """Test that success messages are localized."""
        required_keys = [
            "success.settings_saved",
            "success.language_changed",
            "success.llm_changed",
        ]
        for key in required_keys:
            assert key in STRINGS, f"Missing success message: {key}"


class TestEnglishQuality:
    """Test English string quality."""

    def test_no_korean_in_english_strings(self):
        """Test that English strings don't contain Korean characters."""
        korean_chars = set("가나다라마바사아자차카타파하")
        for key, translations in STRINGS.items():
            english = translations.get("en", "")
            korean_found = any(char in english for char in korean_chars)
            assert not korean_found, f"Korean characters found in English string for {key}: {english}"

    def test_english_capitalization(self):
        """Test that English strings start with capital letter (where appropriate)."""
        exclude_keys = {"misc.yes", "misc.no"}
        for key, translations in STRINGS.items():
            if key in exclude_keys:
                continue
            english = translations.get("en", "")
            if english and english[0].isalpha():
                assert english[0].isupper() or english[0] == "[", f"English string for {key} should start with capital: {english}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
