"""Unit tests for Mode 1 guide generation."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from md_skill_craft.modes.mode1_guide import Mode1Guide
from md_skill_craft.core.base_provider import LLMResponse


class TestMode1Guide:
    """Test Mode 1 guide generator."""

    @pytest.fixture
    def guide(self):
        """Create Mode1Guide instance for testing."""
        with patch("md_skill_craft.modes.mode1_guide.settings") as mock_settings:
            mock_settings.llm = "claude"
            mock_settings.llm_model = "claude-haiku-4-5-20251001"
            mock_settings.language = "en"
            yield Mode1Guide()

    def test_init(self, guide):
        """Test Mode1Guide initialization."""
        assert guide.llm_provider == "claude"
        assert guide.llm_model == "claude-haiku-4-5-20251001"
        assert guide.language == "en"
        assert guide.generated_content is None

    def test_get_file_type_claude(self, guide):
        """Test file type for Claude."""
        guide.llm_provider = "claude"
        assert guide._get_file_type() == "CLAUDE"

    def test_get_file_type_gpt(self, guide):
        """Test file type for GPT."""
        guide.llm_provider = "gpt"
        assert guide._get_file_type() == "AGENT"

    def test_get_file_type_gemini(self, guide):
        """Test file type for Gemini."""
        guide.llm_provider = "gemini"
        assert guide._get_file_type() == "GEMINI"

    def test_get_file_extension(self, guide):
        """Test file extension."""
        guide.llm_provider = "claude"
        assert guide._get_file_extension() == "CLAUDE.md"

        guide.llm_provider = "gpt"
        assert guide._get_file_extension() == "AGENT.md"

    def test_build_system_prompt_korean(self, guide):
        """Test system prompt in Korean."""
        guide.language = "ko"
        prompt = guide._build_system_prompt("CLAUDE")
        assert "CLAUDE.md" in prompt
        assert "당신은" in prompt

    def test_build_system_prompt_english(self, guide):
        """Test system prompt in English."""
        guide.language = "en"
        prompt = guide._build_system_prompt("CLAUDE")
        assert "CLAUDE.md" in prompt
        assert "You are an expert" in prompt

    def test_build_user_message_korean(self, guide):
        """Test user message in Korean."""
        guide.language = "ko"
        project_desc = "FastAPI REST API"
        message = guide._build_user_message(project_desc, "CLAUDE")
        assert project_desc in message
        assert "CLAUDE.md" in message

    def test_build_user_message_english(self, guide):
        """Test user message in English."""
        guide.language = "en"
        project_desc = "FastAPI REST API"
        message = guide._build_user_message(project_desc, "CLAUDE")
        assert project_desc in message
        assert "CLAUDE.md" in message

    @patch("md_skill_craft.modes.mode1_guide.KeyStore")
    def test_get_api_key_from_keystore(self, mock_keystore, guide):
        """Test getting API key from keystore."""
        mock_keystore.get.return_value = "test-key-123"

        key = guide.get_api_key()

        assert key == "test-key-123"
        mock_keystore.get.assert_called_once_with("claude")

    @patch("md_skill_craft.modes.mode1_guide.KeyStore")
    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "env-key-456"})
    def test_get_api_key_from_env(self, mock_keystore, guide):
        """Test getting API key from environment variable."""
        mock_keystore.get.return_value = None

        key = guide.get_api_key()

        assert key == "env-key-456"

    @patch("md_skill_craft.modes.mode1_guide.KeyStore")
    def test_get_api_key_not_found(self, mock_keystore, guide):
        """Test error when API key not found."""
        mock_keystore.get.return_value = None

        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="No API key found"):
                guide.get_api_key()

    def test_save_output_success(self, guide, tmp_path):
        """Test saving output successfully."""
        guide.generated_content = "# Test\n## Project\nTest project"

        result = guide.save_output(tmp_path)

        assert result is True
        saved_file = tmp_path / "CLAUDE.md"
        assert saved_file.exists()
        assert saved_file.read_text() == guide.generated_content

    def test_save_output_no_content(self, guide, tmp_path):
        """Test saving when no content generated."""
        guide.generated_content = None

        result = guide.save_output(tmp_path)

        assert result is False

    def test_save_suggested(self, guide, tmp_path):
        """Test saving as .suggested file."""
        guide.generated_content = "# Test\n## Project\nTest project"

        result = guide.save_suggested(tmp_path)

        assert result is True
        saved_file = tmp_path / "CLAUDE.md.suggested"
        assert saved_file.exists()

    def test_save_output_file_error(self, guide, tmp_path):
        """Test file save error handling."""
        guide.generated_content = "# Test"

        # Create read-only directory
        readonly_path = tmp_path / "readonly"
        readonly_path.mkdir()
        readonly_path.chmod(0o444)

        result = guide.save_output(readonly_path)

        assert result is False

        # Restore permissions for cleanup
        readonly_path.chmod(0o755)

    @patch("md_skill_craft.modes.mode1_guide.ProviderFactory")
    @patch("md_skill_craft.modes.mode1_guide.usage_tracker")
    @patch("md_skill_craft.modes.mode1_guide.progress_bar")
    def test_generate_with_llm(self, mock_progress, mock_tracker, mock_factory, guide):
        """Test LLM generation."""
        # Setup mocks
        mock_response = LLMResponse(
            text="# Test\n## Project\nGenerated content",
            model="claude-haiku",
            provider="claude",
            input_tokens=100,
            output_tokens=50,
        )

        mock_provider = Mock()
        mock_provider.generate.return_value = mock_response
        mock_factory.create.return_value = mock_provider

        mock_progress_context = MagicMock()
        mock_progress_context.__enter__.return_value = (Mock(), 0)
        mock_progress_context.__exit__.return_value = None
        mock_progress.return_value = mock_progress_context

        with patch("md_skill_craft.modes.mode1_guide.KeyStore") as mock_keystore:
            mock_keystore.get.return_value = "test-key"

            result = guide.generate_with_llm("FastAPI project")

        assert "Generated content" in result
        mock_factory.create.assert_called_once()
        mock_tracker.add.assert_called_once_with("claude", 100, 50)

    @patch("md_skill_craft.modes.mode1_guide.ProviderFactory")
    def test_generate_with_llm_error(self, mock_factory, guide):
        """Test LLM generation with error."""
        mock_factory.create.side_effect = Exception("LLM error")

        with patch("md_skill_craft.modes.mode1_guide.KeyStore") as mock_keystore:
            mock_keystore.get.return_value = "test-key"

            result = guide.generate_with_llm("FastAPI project")

        assert result == ""

    def test_collect_project_info(self, guide):
        """Test project info collection."""
        with patch("md_skill_craft.modes.mode1_guide.Menu") as mock_menu:
            mock_menu.prompt.return_value = "FastAPI REST API with PostgreSQL"

            result = guide.collect_project_info()

            assert result == "FastAPI REST API with PostgreSQL"
            mock_menu.prompt.assert_called_once()


class TestMode1GuideIntegration:
    """Integration tests for Mode 1 workflow."""

    @pytest.mark.skip(reason="Requires LLM API - run manually")
    def test_full_workflow(self, tmp_path):
        """Test full Mode 1 workflow with real LLM."""
        # This would require actual API keys
        # Skip in CI/CD, run manually for integration testing
        pass
