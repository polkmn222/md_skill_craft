"""Base LLM provider interface and data structures."""

from dataclasses import dataclass, field
from typing import AsyncIterator, Protocol


@dataclass
class LLMResponse:
    """Response from an LLM provider.

    Attributes:
        text: Generated text response
        model: Model name used for generation
        provider: Provider name (claude, gpt, gemini)
        input_tokens: Number of input tokens consumed
        output_tokens: Number of output tokens generated
        total_tokens: Total tokens (computed property)
    """

    text: str
    model: str
    provider: str
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        """Get total tokens used."""
        return self.input_tokens + self.output_tokens


@dataclass
class LLMConfig:
    """Configuration for LLM generation.

    Attributes:
        model: Model name to use
        temperature: Temperature (0.0-1.0, default 0.7)
        max_tokens: Maximum tokens in response (default 2048)
        system_prompt: System prompt to prepend (optional)
        top_p: Top-p sampling parameter (optional)
        top_k: Top-k sampling parameter (optional)
    """

    model: str
    temperature: float = 0.7
    max_tokens: int = 2048
    system_prompt: str | None = None
    top_p: float | None = None
    top_k: int | None = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert config to dictionary, excluding None values.

        Returns:
            Dictionary representation of config
        """
        result = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if self.system_prompt:
            result["system_prompt"] = self.system_prompt
        if self.top_p is not None:
            result["top_p"] = self.top_p
        if self.top_k is not None:
            result["top_k"] = self.top_k
        return result


class BaseLLMProvider(Protocol):
    """Protocol defining the interface for LLM providers.

    All provider implementations must follow this protocol.
    Uses structural subtyping (duck typing) to avoid explicit inheritance.
    """

    @property
    def name(self) -> str:
        """Get provider name (e.g., 'claude', 'gpt', 'gemini').

        Returns:
            Provider identifier string
        """
        ...

    @property
    def available_models(self) -> list[str]:
        """Get list of available models for this provider.

        Returns:
            List of model names that can be used
        """
        ...

    def generate(
        self,
        prompt: str,
        config: LLMConfig | None = None,
    ) -> LLMResponse:
        """Generate text synchronously (blocking).

        Args:
            prompt: Input text/prompt for generation
            config: Generation configuration (optional, uses defaults if None)

        Returns:
            LLMResponse containing generated text and metadata

        Raises:
            ValueError: If API key not configured or prompt invalid
            Exception: Provider-specific exceptions (rate limits, API errors)

        Example:
            >>> provider = AnthropicProvider(api_key)
            >>> response = provider.generate("Hello, world!")
            >>> print(response.text)
        """
        ...

    async def generate_async(
        self,
        prompt: str,
        config: LLMConfig | None = None,
    ) -> LLMResponse:
        """Generate text asynchronously (non-blocking).

        Args:
            prompt: Input text/prompt for generation
            config: Generation configuration (optional)

        Returns:
            LLMResponse containing generated text and metadata

        Raises:
            ValueError: If API key not configured
            Exception: Provider-specific exceptions

        Example:
            >>> import asyncio
            >>> response = await provider.generate_async("Hello!")
        """
        ...

    async def stream(
        self,
        prompt: str,
        config: LLMConfig | None = None,
    ) -> AsyncIterator[str]:
        """Stream text generation asynchronously, yielding chunks.

        Args:
            prompt: Input text/prompt for generation
            config: Generation configuration (optional)

        Yields:
            Text chunks as they are generated

        Example:
            >>> async for chunk in provider.stream("Hello!"):
            ...     print(chunk, end="", flush=True)
        """
        ...
