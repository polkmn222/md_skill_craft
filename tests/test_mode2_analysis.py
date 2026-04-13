"""Unit tests for Mode 2 project analysis."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from md_skill_craft.modes.mode2_analysis import Mode2Analysis, IGNORED_DIRS
from md_skill_craft.core.base_provider import LLMResponse


class TestMode2Analysis:
    """Test Mode 2 project analyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create Mode2Analysis instance for testing."""
        with patch("md_skill_craft.modes.mode2_analysis.settings") as mock_settings:
            mock_settings.llm = "claude"
            mock_settings.llm_model = "claude-haiku-4-5-20251001"
            mock_settings.language = "en"
            mock_settings.mode = 2
            mock_settings.active_mode = False
            yield Mode2Analysis()

    def test_init(self, analyzer):
        """Test Mode2Analysis initialization."""
        assert analyzer.llm_provider == "claude"
        assert analyzer.llm_model == "claude-haiku-4-5-20251001"
        assert analyzer.language == "en"
        assert analyzer.analysis_results is None
        assert analyzer.active_mode is False

    def test_get_file_type_claude(self, analyzer):
        """Test file type for Claude."""
        analyzer.llm_provider = "claude"
        assert analyzer._get_file_type() == "CLAUDE"

    def test_get_file_type_gpt(self, analyzer):
        """Test file type for GPT."""
        analyzer.llm_provider = "gpt"
        assert analyzer._get_file_type() == "AGENT"

    def test_get_file_type_gemini(self, analyzer):
        """Test file type for Gemini."""
        analyzer.llm_provider = "gemini"
        assert analyzer._get_file_type() == "GEMINI"

    @patch("md_skill_craft.modes.mode2_analysis.KeyStore")
    def test_get_api_key_from_keystore(self, mock_keystore, analyzer):
        """Test getting API key from keystore."""
        mock_keystore.get.return_value = "test-key-123"

        key = analyzer.get_api_key()

        assert key == "test-key-123"
        mock_keystore.get.assert_called_once_with("claude")

    @patch("md_skill_craft.modes.mode2_analysis.KeyStore")
    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "env-key-456"})
    def test_get_api_key_from_env(self, mock_keystore, analyzer):
        """Test getting API key from environment variable."""
        mock_keystore.get.return_value = None

        key = analyzer.get_api_key()

        assert key == "env-key-456"

    @patch("md_skill_craft.modes.mode2_analysis.KeyStore")
    def test_get_api_key_not_found(self, mock_keystore, analyzer):
        """Test error when API key not found."""
        mock_keystore.get.return_value = None

        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="No API key found"):
                analyzer.get_api_key()

    def test_scan_directory_fast_mode(self, analyzer, tmp_path):
        """Test fast mode scanning (key files only)."""
        # Create some files
        (tmp_path / "README.md").write_text("# Test")
        (tmp_path / "pyproject.toml").write_text("# Config")
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("# Code")

        result = analyzer._scan_directory(tmp_path, "fast")

        assert "README.md" in result["key_files"]
        assert "pyproject.toml" in result["key_files"]
        assert len(result["source_dirs"]) == 0
        assert len(result["all_files"]) == 0

    def test_scan_directory_ignores_excluded(self, analyzer, tmp_path):
        """Test that ignored directories are skipped."""
        # Create ignored and non-ignored directories
        (tmp_path / "node_modules").mkdir()
        (tmp_path / "node_modules" / "package.json").write_text("{}")
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / "__pycache__" / "file.pyc").write_text("")
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("# Code")

        result = analyzer._scan_directory(tmp_path, "standard")

        # Should not include anything from ignored directories
        all_found = result["key_files"] + result["source_dirs"]
        assert not any("node_modules" in f for f in all_found)
        assert not any("__pycache__" in f for f in all_found)

    def test_read_existing_config_exists(self, analyzer, tmp_path):
        """Test reading existing config file."""
        config_content = "# CLAUDE.md\n## Project\nTest project"
        (tmp_path / "CLAUDE.md").write_text(config_content)

        result = analyzer._read_existing_config(tmp_path)

        assert result == config_content

    def test_read_existing_config_not_found(self, analyzer, tmp_path):
        """Test when config file doesn't exist."""
        result = analyzer._read_existing_config(tmp_path)

        assert result is None

    def test_build_system_prompt_korean(self, analyzer):
        """Test system prompt in Korean."""
        analyzer.language = "ko"
        prompt = analyzer._build_system_prompt()
        assert "전문가" in prompt
        assert "분석" in prompt

    def test_build_system_prompt_english(self, analyzer):
        """Test system prompt in English."""
        analyzer.language = "en"
        prompt = analyzer._build_system_prompt()
        assert "expert" in prompt
        assert "analyze" in prompt.lower()

    def test_build_user_message_with_config(self, analyzer):
        """Test user message building with existing config."""
        analyzer.language = "en"
        project_info = "README.md\nsrc/main.py"
        existing_config = "# CLAUDE.md\n## Project\nTest"

        message = analyzer._build_user_message("test-project", project_info, existing_config)

        assert "test-project" in message
        assert "project_info" in message.lower() or project_info in message
        assert existing_config in message

    def test_build_user_message_without_config(self, analyzer):
        """Test user message building without existing config."""
        analyzer.language = "en"
        project_info = "README.md\nsrc/main.py"

        message = analyzer._build_user_message("test-project", project_info, None)

        assert "test-project" in message
        assert "No existing" in message or "configuration file" in message

    def test_save_analysis_success(self, analyzer, tmp_path):
        """Test saving analysis results."""
        analyzer.analysis_results = "# Analysis\n## Issues\nNone"
        analyzer.llm_provider = "claude"

        result = analyzer.save_analysis(tmp_path)

        assert result is True
        saved_file = tmp_path / "CLAUDE.md.suggested"
        assert saved_file.exists()
        assert "Analysis" in saved_file.read_text()

    def test_save_analysis_no_results(self, analyzer, tmp_path):
        """Test saving when no results available."""
        analyzer.analysis_results = None

        result = analyzer.save_analysis(tmp_path)

        assert result is False

    def test_save_analysis_file_error(self, analyzer, tmp_path):
        """Test save error handling."""
        analyzer.analysis_results = "# Test"
        analyzer.llm_provider = "claude"

        # Create read-only directory
        readonly_path = tmp_path / "readonly"
        readonly_path.mkdir()
        readonly_path.chmod(0o444)

        result = analyzer.save_analysis(readonly_path)

        assert result is False

        # Restore permissions for cleanup
        readonly_path.chmod(0o755)

    @patch("md_skill_craft.modes.mode2_analysis.ProviderFactory")
    @patch("md_skill_craft.modes.mode2_analysis.usage_tracker")
    @patch("md_skill_craft.modes.mode2_analysis.progress_bar")
    def test_analyze_with_llm(self, mock_progress, mock_tracker, mock_factory, analyzer):
        """Test LLM analysis."""
        # Setup mocks
        mock_response = LLMResponse(
            text="# Analysis\n## Issues\nNone found",
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

        with patch("md_skill_craft.modes.mode2_analysis.KeyStore") as mock_keystore:
            mock_keystore.get.return_value = "test-key"

            result = analyzer.analyze_with_llm(
                Path("/test"),
                "README.md\nsrc/",
                None
            )

        assert "Analysis" in result
        mock_factory.create.assert_called_once()
        mock_tracker.add.assert_called_once_with("claude", 100, 50)

    @patch("md_skill_craft.modes.mode2_analysis.ProviderFactory")
    def test_analyze_with_llm_error(self, mock_factory, analyzer):
        """Test LLM analysis with error."""
        mock_factory.create.side_effect = Exception("LLM error")

        with patch("md_skill_craft.modes.mode2_analysis.KeyStore") as mock_keystore:
            mock_keystore.get.return_value = "test-key"

            result = analyzer.analyze_with_llm(
                Path("/test"),
                "README.md",
                None
            )

        assert result == ""

    def test_select_analysis_depth(self, analyzer):
        """Test depth selection menu."""
        with patch("md_skill_craft.modes.mode2_analysis.Menu") as mock_menu:
            mock_menu.select.return_value = 2

            result = analyzer.select_analysis_depth()

            assert result == "standard"

    def test_select_analysis_depth_deep(self, analyzer):
        """Test selecting deep analysis."""
        with patch("md_skill_craft.modes.mode2_analysis.Menu") as mock_menu:
            mock_menu.select.return_value = 3

            result = analyzer.select_analysis_depth()

            assert result == "deep"

    def test_ignored_dirs_constant(self):
        """Test that IGNORED_DIRS contains expected directories."""
        assert "node_modules" in IGNORED_DIRS
        assert "__pycache__" in IGNORED_DIRS
        assert ".git" in IGNORED_DIRS
        assert ".venv" in IGNORED_DIRS


class TestMode2AnalysisIntegration:
    """Integration tests for Mode 2 workflow."""

    @pytest.mark.skip(reason="Requires LLM API - run manually")
    def test_full_workflow(self, tmp_path):
        """Test full Mode 2 workflow with real LLM."""
        # This would require actual API keys
        # Skip in CI/CD, run manually for integration testing
        pass
