"""Anthropic Claude API provider implementation."""

from typing import AsyncIterator

import anthropic

from md_skill_craft.core.base_provider import LLMConfig, LLMResponse


class AnthropicProvider:
    """Claude API provider using Anthropic SDK.

    Supports streaming and async generation. Uses Claude models for generation.
    """

    def __init__(self, api_key: str) -> None:
        """Initialize provider with API key.

        Args:
            api_key: Anthropic API key
        """
        self._client = anthropic.Anthropic(api_key=api_key)
        self._async_client = anthropic.AsyncAnthropic(api_key=api_key)
        self._name = "claude"

    @property
    def name(self) -> str:
        """Get provider name."""
        return self._name

    @property
    def available_models(self) -> list[str]:
        """Get list of available Claude models.

        Returns:
            List of supported Claude model names
        """
        return [
            "claude-opus-4-6",        # Most capable, highest cost
            "claude-sonnet-4-6",      # Balanced capability/cost
            "claude-haiku-4-5",       # Fastest, most cost-effective
        ]

    def generate(
        self,
        prompt: str,
        config: LLMConfig | None = None,
    ) -> LLMResponse:
        """Generate text synchronously using Claude API.

        Args:
            prompt: Input text/prompt
            config: Generation configuration

        Returns:
            LLMResponse with generated text and token counts

        Raises:
            anthropic.APIError: If API call fails
            ValueError: If prompt is empty
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        cfg = config or LLMConfig(model=self.available_models[0])

        # Build message
        messages = [{"role": "user", "content": prompt}]

        # Build kwargs
        kwargs: dict = {
            "model": cfg.model,
            "max_tokens": cfg.max_tokens,
            "messages": messages,
            "temperature": cfg.temperature,
        }

        if cfg.system_prompt:
            kwargs["system"] = cfg.system_prompt
        if cfg.top_p is not None:
            kwargs["top_p"] = cfg.top_p

        # Call API
        response = self._client.messages.create(**kwargs)

        # Extract response
        text = response.content[0].text

        return LLMResponse(
            text=text,
            model=cfg.model,
            provider=self.name,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

    async def generate_async(
        self,
        prompt: str,
        config: LLMConfig | None = None,
    ) -> LLMResponse:
        """Generate text asynchronously using Claude API.

        Args:
            prompt: Input text/prompt
            config: Generation configuration

        Returns:
            LLMResponse with generated text and token counts

        Raises:
            anthropic.APIError: If API call fails
            ValueError: If prompt is empty
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        cfg = config or LLMConfig(model=self.available_models[0])

        # Build message
        messages = [{"role": "user", "content": prompt}]

        # Build kwargs
        kwargs: dict = {
            "model": cfg.model,
            "max_tokens": cfg.max_tokens,
            "messages": messages,
            "temperature": cfg.temperature,
        }

        if cfg.system_prompt:
            kwargs["system"] = cfg.system_prompt
        if cfg.top_p is not None:
            kwargs["top_p"] = cfg.top_p

        # Call API async
        response = await self._async_client.messages.create(**kwargs)

        # Extract response
        text = response.content[0].text

        return LLMResponse(
            text=text,
            model=cfg.model,
            provider=self.name,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

    async def stream(
        self,
        prompt: str,
        config: LLMConfig | None = None,
    ) -> AsyncIterator[str]:
        """Stream text generation asynchronously.

        Args:
            prompt: Input text/prompt
            config: Generation configuration

        Yields:
            Text chunks as they arrive from the API

        Raises:
            anthropic.APIError: If API call fails
            ValueError: If prompt is empty
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        cfg = config or LLMConfig(model=self.available_models[0])

        # Build message
        messages = [{"role": "user", "content": prompt}]

        # Build kwargs
        kwargs: dict = {
            "model": cfg.model,
            "max_tokens": cfg.max_tokens,
            "messages": messages,
            "temperature": cfg.temperature,
        }

        if cfg.system_prompt:
            kwargs["system"] = cfg.system_prompt
        if cfg.top_p is not None:
            kwargs["top_p"] = cfg.top_p

        # Stream from API
        with self._client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield text
