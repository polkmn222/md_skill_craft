"""API pricing and cost calculation for different LLM models."""

# Pricing per 1 million tokens (as of 2025-04-13)
PRICING_PER_1M: dict[str, dict[str, float]] = {
    # Claude (Anthropic)
    "claude-opus-4-6": {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5-20251001": {"input": 0.80, "output": 4.00},
    # GPT (OpenAI)
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    # Gemini (Google)
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    "gemini-2.0-pro": {"input": 1.25, "output": 5.00},
}


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate API cost for given model and token usage.

    Args:
        model: Model name (e.g., "claude-haiku-4-5-20251001")
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Cost in USD as float
    """
    if model not in PRICING_PER_1M:
        return 0.0

    prices = PRICING_PER_1M[model]
    return (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1_000_000


def get_all_models() -> list[str]:
    """Get list of all available models.

    Returns:
        List of model names
    """
    return list(PRICING_PER_1M.keys())


def get_models_by_provider(provider: str) -> list[str]:
    """Get list of models for specific provider.

    Args:
        provider: Provider name ("claude", "gpt", or "gemini")

    Returns:
        List of model names for the provider
    """
    prefix_map = {
        "claude": "claude-",
        "gpt": "gpt-",
        "gemini": "gemini-",
    }

    if provider not in prefix_map:
        return []

    prefix = prefix_map[provider]
    return [m for m in PRICING_PER_1M.keys() if m.startswith(prefix)]
