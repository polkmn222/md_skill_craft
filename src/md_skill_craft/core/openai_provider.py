"""OpenAI GPT API provider implementation."""

from typing import AsyncIterator

from openai import AsyncOpenAI, OpenAI

from md_skill_craft.core.base_provider import LLMConfig, LLMResponse


class OpenAIProvider:
    """OpenAI GPT API provider using OpenAI SDK.

    Supports streaming and async generation. Uses GPT models for generation.
    """

    def __init__(self, api_key: str) -> None:
        """Initialize provider with API key.

        Args:
            api_key: OpenAI API key
        """
        self._client = OpenAI(api_key=api_key)
        self._async_client = AsyncOpenAI(api_key=api_key)
        self._name = "gpt"

    @property
    def name(self) -> str:
        """Get provider name."""
        return self._name

    @property
    def available_models(self) -> list[str]:
        """Get list of available GPT models.

        Returns:
            List of supported GPT model names
        """
        return [
            "gpt-4o",            # Most capable
            "gpt-4-turbo",       # High capability, faster
            "gpt-4o-mini",       # Efficient, low-cost
        ]

    def generate(
        self,
        prompt: str,
        config: LLMConfig | None = None,
    ) -> LLMResponse:
        """Generate text synchronously using OpenAI API.

        Args:
            prompt: Input text/prompt
            config: Generation configuration

        Returns:
            LLMResponse with generated text and token counts

        Raises:
            openai.APIError: If API call fails
            ValueError: If prompt is empty
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        cfg = config or LLMConfig(model=self.available_models[0])

        # Build messages
        messages = []
        if cfg.system_prompt:
            messages.append({"role": "system", "content": cfg.system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Build kwargs
        kwargs: dict = {
            "model": cfg.model,
            "max_tokens": cfg.max_tokens,
            "messages": messages,
            "temperature": cfg.temperature,
        }

        if cfg.top_p is not None:
            kwargs["top_p"] = cfg.top_p

        # Call API
        response = self._client.chat.completions.create(**kwargs)

        # Extract response
        text = response.choices[0].message.content or ""

        return LLMResponse(
            text=text,
            model=cfg.model,
            provider=self.name,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
        )

    async def generate_async(
        self,
        prompt: str,
        config: LLMConfig | None = None,
    ) -> LLMResponse:
        """Generate text asynchronously using OpenAI API.

        Args:
            prompt: Input text/prompt
            config: Generation configuration

        Returns:
            LLMResponse with generated text and token counts

        Raises:
            openai.APIError: If API call fails
            ValueError: If prompt is empty
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        cfg = config or LLMConfig(model=self.available_models[0])

        # Build messages
        messages = []
        if cfg.system_prompt:
            messages.append({"role": "system", "content": cfg.system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Build kwargs
        kwargs: dict = {
            "model": cfg.model,
            "max_tokens": cfg.max_tokens,
            "messages": messages,
            "temperature": cfg.temperature,
        }

        if cfg.top_p is not None:
            kwargs["top_p"] = cfg.top_p

        # Call API async
        response = await self._async_client.chat.completions.create(**kwargs)

        # Extract response
        text = response.choices[0].message.content or ""

        return LLMResponse(
            text=text,
            model=cfg.model,
            provider=self.name,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
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
            openai.APIError: If API call fails
            ValueError: If prompt is empty
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        cfg = config or LLMConfig(model=self.available_models[0])

        # Build messages
        messages = []
        if cfg.system_prompt:
            messages.append({"role": "system", "content": cfg.system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Build kwargs
        kwargs: dict = {
            "model": cfg.model,
            "max_tokens": cfg.max_tokens,
            "messages": messages,
            "temperature": cfg.temperature,
        }

        if cfg.top_p is not None:
            kwargs["top_p"] = cfg.top_p

        # Stream from API
        async with await self._async_client.chat.completions.create(
            stream=True,
            **kwargs,
        ) as response:
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
