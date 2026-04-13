"""Shared pytest configuration and fixtures."""

import pytest
from unittest.mock import Mock

from md_skill_craft.core.base_provider import BaseLLMProvider, LLMResponse
from md_skill_craft.core.provider_factory import ProviderFactory


@pytest.fixture
def mock_provider() -> Mock:
    """Fixture: Mock LLM provider for testing.

    Returns:
        Mock provider implementing BaseLLMProvider protocol
    """
    provider = Mock(spec=BaseLLMProvider)
    provider.name = "mock"
    provider.available_models = ["mock-model"]

    # Default response
    default_response = LLMResponse(
        text="Mock response",
        model="mock-model",
        provider="mock",
        input_tokens=10,
        output_tokens=20,
    )
    provider.generate.return_value = default_response

    return provider


@pytest.fixture
def sample_response() -> LLMResponse:
    """Fixture: Sample LLM response for testing.

    Returns:
        Sample LLMResponse object
    """
    return LLMResponse(
        text="This is a sample response from the LLM.",
        model="claude-haiku-4-5",
        provider="claude",
        input_tokens=15,
        output_tokens=25,
    )
