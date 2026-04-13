"""Google Gemini API provider implementation."""

from typing import AsyncIterator

import google.genai as genai

from md_skill_craft.core.base_provider import LLMConfig, LLMResponse


class GoogleProvider:
    """Google Gemini API provider using google-genai SDK.

    Supports streaming and async generation. Uses Gemini models for generation.
    Note: Uses the new google-genai SDK (not google-generativeai which is deprecated).
    """

    def __init__(self, api_key: str) -> None:
        """Initialize provider with API key.

        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self._client = genai.client.Client()
        self._name = "gemini"

    @property
    def name(self) -> str:
        """Get provider name."""
        return self._name

    @property
    def available_models(self) -> list[str]:
        """Get list of available Gemini models.

        Returns:
            List of supported Gemini model names
        """
        return [
            "gemini-3-pro",              # Most capable
            "gemini-3-flash",            # Balanced
            "gemini-3-flash-preview",    # Latest preview
        ]

    def generate(
        self,
        prompt: str,
        config: LLMConfig | None = None,
    ) -> LLMResponse:
        """Generate text synchronously using Gemini API.

        Args:
            prompt: Input text/prompt
            config: Generation configuration

        Returns:
            LLMResponse with generated text and token counts

        Raises:
            Exception: If API call fails
            ValueError: If prompt is empty
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        cfg = config or LLMConfig(model=self.available_models[0])

        # Build generation config
        gen_config = {
            "temperature": cfg.temperature,
            "max_output_tokens": cfg.max_tokens,
        }
        if cfg.top_p is not None:
            gen_config["top_p"] = cfg.top_p
        if cfg.top_k is not None:
            gen_config["top_k"] = cfg.top_k

        # Build system instruction
        system_instruction = cfg.system_prompt or ""

        # Call API
        response = self._client.models.generate_content(
            model=cfg.model,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                **gen_config,
                system_instruction=system_instruction if system_instruction else None,
            ),
        )

        # Extract response
        text = response.text or ""

        # Note: google-genai doesn't always provide token counts,
        # so we use 0 as placeholder
        return LLMResponse(
            text=text,
            model=cfg.model,
            provider=self.name,
            input_tokens=0,
            output_tokens=0,
        )

    async def generate_async(
        self,
        prompt: str,
        config: LLMConfig | None = None,
    ) -> LLMResponse:
        """Generate text asynchronously using Gemini API.

        Args:
            prompt: Input text/prompt
            config: Generation configuration

        Returns:
            LLMResponse with generated text and token counts

        Raises:
            Exception: If API call fails
            ValueError: If prompt is empty

        Note:
            google-genai SDK has limited async support.
            This currently calls the sync method in an async context.
        """
        # google-genai has limited async support, so we call sync method
        return self.generate(prompt, config)

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
            Exception: If API call fails
            ValueError: If prompt is empty

        Note:
            google-genai streaming support is limited in async context.
            This implementation yields the full response in one chunk.
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        cfg = config or LLMConfig(model=self.available_models[0])

        # Build generation config
        gen_config = {
            "temperature": cfg.temperature,
            "max_output_tokens": cfg.max_tokens,
        }
        if cfg.top_p is not None:
            gen_config["top_p"] = cfg.top_p
        if cfg.top_k is not None:
            gen_config["top_k"] = cfg.top_k

        # Build system instruction
        system_instruction = cfg.system_prompt or ""

        # Call API (streaming support in google-genai is limited)
        response = self._client.models.generate_content(
            model=cfg.model,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                **gen_config,
                system_instruction=system_instruction if system_instruction else None,
            ),
        )

        # Yield the full response as one chunk
        text = response.text or ""
        yield text
