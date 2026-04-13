"""API key storage using system keyring."""

import keyring
from typing import Optional

SERVICE_NAME = "md-skill-craft"


class KeyStore:
    """Manage API keys using system keyring (Keychain/Credential Manager/libsecret)."""

    @staticmethod
    def save(provider: str, api_key: str) -> None:
        """Save API key to system keyring.

        Args:
            provider: Provider name ("claude", "gpt", "gemini")
            api_key: API key to save
        """
        try:
            keyring.set_password(SERVICE_NAME, provider, api_key)
        except Exception as e:
            # Fallback if keyring fails (e.g., in CI/CD environments)
            print(f"Warning: Could not save key to system keyring: {e}")

    @staticmethod
    def get(provider: str) -> Optional[str]:
        """Get API key from system keyring.

        Args:
            provider: Provider name ("claude", "gpt", "gemini")

        Returns:
            API key if found, None otherwise
        """
        try:
            return keyring.get_password(SERVICE_NAME, provider)
        except Exception:
            return None

    @staticmethod
    def delete(provider: str) -> None:
        """Delete API key from system keyring.

        Args:
            provider: Provider name ("claude", "gpt", "gemini")
        """
        try:
            keyring.delete_password(SERVICE_NAME, provider)
        except Exception:
            pass

    @staticmethod
    def has_key(provider: str) -> bool:
        """Check if API key exists in system keyring.

        Args:
            provider: Provider name ("claude", "gpt", "gemini")

        Returns:
            True if key exists, False otherwise
        """
        return KeyStore.get(provider) is not None
