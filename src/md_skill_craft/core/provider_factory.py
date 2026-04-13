"""Factory for creating and managing LLM provider instances."""

from md_skill_craft.config.settings import settings
from md_skill_craft.core.anthropic_provider import AnthropicProvider
from md_skill_craft.core.base_provider import BaseLLMProvider
from md_skill_craft.core.google_provider import GoogleProvider
from md_skill_craft.core.openai_provider import OpenAIProvider


class ProviderFactory:
    """Factory for creating LLM provider instances.

    Provides methods to:
    - Create provider instances
    - List available providers based on configured API keys
    - Get default provider
    """

    @staticmethod
    def create(provider_name: str, api_key: str) -> BaseLLMProvider:
        """Create a provider instance.

        Args:
            provider_name: Name of provider ('claude', 'gpt', 'gemini')
            api_key: API key for the provider

        Returns:
            Provider instance implementing BaseLLMProvider protocol

        Raises:
            ValueError: If provider_name is unknown

        Example:
            >>> factory = ProviderFactory()
            >>> provider = factory.create('claude', api_key)
            >>> response = provider.generate('Hello!')
        """
        match provider_name.lower():
            case "claude" | "anthropic":
                return AnthropicProvider(api_key)
            case "gpt" | "openai":
                return OpenAIProvider(api_key)
            case "gemini" | "google":
                return GoogleProvider(api_key)
            case _:
                raise ValueError(
                    f"Unknown provider: {provider_name}. "
                    "Choose from: 'claude', 'gpt', 'gemini'"
                )

    @staticmethod
    def available_from_env() -> dict[str, str]:
        """Get all available providers based on configured API keys in .env.

        Returns:
            Dictionary mapping provider names to API keys.
            Only includes providers with configured keys.

        Example:
            >>> providers = ProviderFactory.available_from_env()
            >>> providers
            {'claude': 'sk-ant-...', 'gpt': 'sk-...'}
        """
        return settings.available_providers()

    @staticmethod
    def create_default() -> BaseLLMProvider:
        """Create the default provider based on settings.

        Returns:
            Default provider instance

        Raises:
            ValueError: If no API keys configured or default provider not available

        Example:
            >>> provider = ProviderFactory.create_default()
            >>> response = provider.generate('Hello!')
        """
        available = ProviderFactory.available_from_env()
        if not available:
            raise ValueError(
                "No API keys configured. Please set at least one API key in .env file: "
                "ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY"
            )

        default = settings.default_provider
        if default not in available:
            # Fallback to first available
            default = list(available.keys())[0]

        return ProviderFactory.create(default, available[default])

    @staticmethod
    def list_providers() -> list[str]:
        """List names of all available providers.

        Returns:
            List of provider names that have configured API keys

        Example:
            >>> providers = ProviderFactory.list_providers()
            >>> providers
            ['claude', 'gpt']
        """
        return list(ProviderFactory.available_from_env().keys())

    @staticmethod
    def get_provider_and_model(provider_name: str) -> tuple[BaseLLMProvider, str]:
        """Get a provider instance and its default model.

        Args:
            provider_name: Name of provider

        Returns:
            Tuple of (provider_instance, default_model_name)

        Raises:
            ValueError: If provider not available

        Example:
            >>> provider, model = ProviderFactory.get_provider_and_model('claude')
            >>> model
            'claude-haiku-4-5'
        """
        available = ProviderFactory.available_from_env()
        if provider_name not in available:
            raise ValueError(
                f"Provider '{provider_name}' not available. "
                f"Available: {list(available.keys())}"
            )

        provider = ProviderFactory.create(provider_name, available[provider_name])
        model = settings.get_model(provider_name)
        return provider, model
