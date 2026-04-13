"""User settings and configuration management."""

import json
from pathlib import Path
from typing import Literal, Optional
from platformdirs import user_config_dir

CONFIG_DIR = Path(user_config_dir("md-skill-craft"))
CONFIG_FILE = CONFIG_DIR / "config.json"
USAGE_FILE = CONFIG_DIR / "usage.json"


class Settings:
    """Manage user settings and configuration."""

    def __init__(self) -> None:
        """Initialize settings."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self._config: dict = self._load_config()

    def _load_config(self) -> dict:
        """Load config from file or return defaults.

        Returns:
            Configuration dictionary
        """
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return self._default_config()
        return self._default_config()

    @staticmethod
    def _default_config() -> dict:
        """Get default configuration.

        Returns:
            Default config dictionary
        """
        return {
            "language": None,  # "ko" or "en"
            "mode": None,  # 1 or 2
            "llm": None,  # "claude", "gpt", "gemini"
            "llm_model": None,  # Specific model name
            "active_mode": None,  # True (active) or False (passive), only for mode 2
            "use_env_var": True,  # Prefer environment variables for API keys
        }

    def save(self) -> None:
        """Save config to file."""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")

    def set(self, key: str, value: any) -> None:
        """Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value

    def get(self, key: str, default: any = None) -> any:
        """Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)

    @property
    def is_first_run(self) -> bool:
        """Check if this is first run (config not complete).

        Returns:
            True if language not set (onboarding incomplete)
        """
        return self._config.get("language") is None

    @property
    def language(self) -> Optional[str]:
        """Get selected language."""
        return self._config.get("language")

    @language.setter
    def language(self, value: str) -> None:
        """Set selected language."""
        self._config["language"] = value

    @property
    def mode(self) -> Optional[int]:
        """Get selected mode (1 or 2)."""
        return self._config.get("mode")

    @mode.setter
    def mode(self, value: int) -> None:
        """Set selected mode."""
        if value not in (1, 2):
            raise ValueError("Mode must be 1 or 2")
        self._config["mode"] = value

    @property
    def llm(self) -> Optional[str]:
        """Get selected LLM provider."""
        return self._config.get("llm")

    @llm.setter
    def llm(self, value: str) -> None:
        """Set selected LLM provider."""
        if value not in ("claude", "gpt", "gemini"):
            raise ValueError("LLM must be 'claude', 'gpt', or 'gemini'")
        self._config["llm"] = value

    @property
    def llm_model(self) -> Optional[str]:
        """Get selected LLM model."""
        return self._config.get("llm_model")

    @llm_model.setter
    def llm_model(self, value: str) -> None:
        """Set selected LLM model."""
        self._config["llm_model"] = value

    @property
    def active_mode(self) -> Optional[bool]:
        """Get active/passive mode (for mode 2)."""
        return self._config.get("active_mode")

    @active_mode.setter
    def active_mode(self, value: bool) -> None:
        """Set active/passive mode."""
        self._config["active_mode"] = value

    @property
    def use_env_var(self) -> bool:
        """Get whether to prefer environment variables for API keys."""
        return self._config.get("use_env_var", True)

    @use_env_var.setter
    def use_env_var(self, value: bool) -> None:
        """Set whether to prefer environment variables."""
        self._config["use_env_var"] = value

    def reset(self) -> None:
        """Reset settings to defaults."""
        self._config = self._default_config()


class UsageTracker:
    """Track API token usage for cost calculation."""

    def __init__(self) -> None:
        """Initialize usage tracker."""
        self._usage: dict = self._load_usage()

    def _load_usage(self) -> dict:
        """Load usage from file or return empty dict.

        Returns:
            Usage dictionary
        """
        if USAGE_FILE.exists():
            try:
                with open(USAGE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return self._default_usage()
        return self._default_usage()

    @staticmethod
    def _default_usage() -> dict:
        """Get default usage structure.

        Returns:
            Default usage dictionary
        """
        return {
            "claude": {"input_tokens": 0, "output_tokens": 0},
            "gpt": {"input_tokens": 0, "output_tokens": 0},
            "gemini": {"input_tokens": 0, "output_tokens": 0},
        }

    def save(self) -> None:
        """Save usage to file."""
        try:
            with open(USAGE_FILE, "w", encoding="utf-8") as f:
                json.dump(self._usage, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save usage: {e}")

    def add(self, provider: str, input_tokens: int, output_tokens: int) -> None:
        """Record API usage.

        Args:
            provider: Provider name ("claude", "gpt", "gemini")
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        """
        if provider not in self._usage:
            self._usage[provider] = {"input_tokens": 0, "output_tokens": 0}

        self._usage[provider]["input_tokens"] += input_tokens
        self._usage[provider]["output_tokens"] += output_tokens

    def get(self, provider: str) -> dict:
        """Get usage for a provider.

        Args:
            provider: Provider name

        Returns:
            Usage dictionary with "input_tokens" and "output_tokens"
        """
        if provider not in self._usage:
            return {"input_tokens": 0, "output_tokens": 0}
        return self._usage[provider]

    def get_all(self) -> dict:
        """Get all usage data.

        Returns:
            Complete usage dictionary
        """
        return self._usage

    def reset(self) -> None:
        """Reset usage tracking."""
        self._usage = self._default_usage()


# Global instances
settings = Settings()
usage_tracker = UsageTracker()
