---
name: Orchestration & Design Patterns
description: Provider Factory, Feature Router, error handling chains, composition patterns
type: reference
---

# Orchestration Patterns Guide

How to structure code for flexibility, testability, and maintainability using factories, protocols, and composition.

## Single vs. Multi-Agent Architecture

### Single-Agent (This Project)
- **One provider** does all work (Claude, GPT, or Gemini)
- **Simple flow**: User input → Model call → Output
- **Advantage**: Easy to understand, deploy, debug
- **When to use**: Simple tasks, single decision point

```
User Input
    ↓
[Provider: Claude/GPT/Gemini]
    ↓
Output
```

### Multi-Agent (Future Extension)
- **Multiple AI agents** collaborate on complex tasks
- **Orchestrator** routes work between agents
- **Advantage**: Can decompose hard problems
- **When to use**: Complex workflows, specialized agents

```
User Input
    ↓
[Orchestrator: Claude]
    ↓ (routes to specialists)
┌───────┬──────────┬────────┐
↓       ↓          ↓        ↓
[Code] [Doc]   [Test]  [Review]
 Gen   Gen      Gen      Agent
    └───────┬──────────┬────────┘
            ↓
        [Claude] Synthesizes
            ↓
        Output
```

## Pattern 1: Factory Pattern

Used to abstract away provider creation. Clients don't need to know which provider to use.

### Simple Factory

```python
from typing import Literal

class ProviderFactory:
    @staticmethod
    def create(provider_name: str, api_key: str) -> BaseLLMProvider:
        """Create a provider instance."""
        match provider_name.lower():
            case "claude":
                return AnthropicProvider(api_key)
            case "gpt":
                return OpenAIProvider(api_key)
            case "gemini":
                return GoogleProvider(api_key)
            case _:
                raise ValueError(f"Unknown provider: {provider_name}")

    @staticmethod
    def available_from_env() -> dict[str, str]:
        """Get available providers from environment."""
        from app.config import settings
        return settings.available_providers()

# Usage
available = ProviderFactory.available_from_env()
provider = ProviderFactory.create("claude", available["claude"])
response = provider.generate("Hello!")
```

### Factory With Dependency Injection

```python
class Service:
    def __init__(self, provider: BaseLLMProvider) -> None:
        """Inject provider at init time."""
        self._provider = provider

    def process(self, query: str) -> str:
        """Use injected provider."""
        response = self._provider.generate(query)
        return response.text

# Usage
provider = ProviderFactory.create_default()
service = Service(provider)
result = service.process("What is AI?")
```

## Pattern 2: Strategy Pattern

Different algorithms (strategies) for the same task. Swap at runtime.

```python
from typing import Protocol

class TranslationStrategy(Protocol):
    """Strategy for translating text."""
    def translate(self, text: str, source: str, target: str) -> str: ...

class DirectTranslation:
    """Direct translation via LLM."""
    def __init__(self, provider: BaseLLMProvider) -> None:
        self._provider = provider
    
    def translate(self, text: str, source: str, target: str) -> str:
        prompt = f"Translate from {source} to {target}: {text}"
        response = self._provider.generate(prompt)
        return response.text

class BackTranslation:
    """Translate via intermediate language to improve quality."""
    def __init__(self, provider: BaseLLMProvider) -> None:
        self._provider = provider
    
    def translate(self, text: str, source: str, target: str) -> str:
        # source → English → target
        en = self._provider.generate(f"Translate to English: {text}").text
        result = self._provider.generate(f"Translate from English to {target}: {en}").text
        return result

class Translator:
    def __init__(self, strategy: TranslationStrategy) -> None:
        """Inject strategy."""
        self._strategy = strategy
    
    def translate(self, text: str, source: str, target: str) -> str:
        """Delegate to strategy."""
        return self._strategy.translate(text, source, target)

# Usage: Swap strategies
provider = ProviderFactory.create_default()

# Simple approach
simple = Translator(DirectTranslation(provider))
result1 = simple.translate("Hello", "en", "ko")

# Better quality
advanced = Translator(BackTranslation(provider))
result2 = advanced.translate("Hello", "en", "ko")
```

## Pattern 3: Error Handling Chain

Handle errors gracefully with fallbacks.

```python
from typing import TypeVar, Callable

T = TypeVar("T")

class ErrorHandler:
    def __init__(self, func: Callable[[], T]) -> None:
        self._func = func
        self._handlers: list[tuple[type, Callable]] = []
    
    def handle(
        self,
        exception_type: type,
        handler: Callable[[Exception], T],
    ) -> "ErrorHandler":
        """Register an error handler."""
        self._handlers.append((exception_type, handler))
        return self
    
    def execute(self) -> T:
        """Execute with error handling chain."""
        try:
            return self._func()
        except Exception as e:
            for exc_type, handler in self._handlers:
                if isinstance(e, exc_type):
                    return handler(e)
            raise  # Re-raise if no handler

# Usage
def translate(text: str) -> str:
    """Translate with fallback to alternative provider."""
    def primary():
        provider = ProviderFactory.create("claude", api_key)
        return provider.generate(text).text
    
    def handle_api_error(e: Exception) -> str:
        logger.warning(f"Claude API failed: {e}, trying GPT...")
        provider = ProviderFactory.create("gpt", openai_api_key)
        return provider.generate(text).text
    
    def handle_rate_limit(e: Exception) -> str:
        logger.error("Rate limited, returning cached result")
        return cache.get(f"translation:{text}", "Translation unavailable")
    
    return (
        ErrorHandler(primary)
        .handle(RateLimitError, handle_rate_limit)
        .handle(APIError, handle_api_error)
        .execute()
    )
```

## Pattern 4: Feature Router

Route requests to different handlers based on feature type.

```python
from enum import Enum
from typing import Callable

class Feature(Enum):
    """Available features."""
    TRANSLATE = "translate"
    PRACTICE = "practice"
    DOC_WRITE = "doc_write"

class FeatureRouter:
    """Routes requests to feature handlers."""
    
    def __init__(self, provider: BaseLLMProvider) -> None:
        self._provider = provider
        self._handlers: dict[Feature, Callable] = {
            Feature.TRANSLATE: self._handle_translate,
            Feature.PRACTICE: self._handle_practice,
            Feature.DOC_WRITE: self._handle_doc_write,
        }
    
    def route(self, feature: Feature, **kwargs) -> str:
        """Route request to appropriate handler."""
        handler = self._handlers.get(feature)
        if not handler:
            raise ValueError(f"Unknown feature: {feature}")
        return handler(**kwargs)
    
    def _handle_translate(self, text: str, source: str, target: str) -> str:
        translator = Translator(self._provider)
        result = translator.translate(TranslationRequest(text, source, target))
        return result.text
    
    def _handle_practice(self, task: str, technique: str) -> str:
        practice = PromptPractice(self._provider)
        result = practice.execute(PromptPracticeRequest(task, technique))
        return result.text
    
    def _handle_doc_write(self, content: str, doc_type: str) -> str:
        writer = DocWriter(self._provider)
        result = writer.write(DocWriteRequest(content, doc_type))
        return result.text

# Usage
provider = ProviderFactory.create_default()
router = FeatureRouter(provider)

# Route to different handlers
result1 = router.route(Feature.TRANSLATE, text="안녕", source="ko", target="en")
result2 = router.route(Feature.PRACTICE, task="What is 2+2?", technique="zero-shot")
```

## Pattern 5: Adapter Pattern

Adapt incompatible interfaces to work together.

```python
class OldLLMAPI:
    """Legacy LLM interface we want to replace."""
    def call(self, prompt: str) -> str:
        """Old method signature."""
        pass

class LLMAdapter:
    """Adapt OldLLMAPI to BaseLLMProvider interface."""
    
    def __init__(self, old_api: OldLLMAPI) -> None:
        self._api = old_api
    
    @property
    def name(self) -> str:
        return "legacy"
    
    @property
    def available_models(self) -> list[str]:
        return ["legacy-v1"]
    
    def generate(self, prompt: str, config: LLMConfig | None = None) -> LLMResponse:
        """Adapt old API to new interface."""
        text = self._api.call(prompt)
        return LLMResponse(
            text=text,
            model="legacy-v1",
            provider="legacy",
        )

# Usage: Works with existing code
old_api = OldLLMAPI()
new_provider = LLMAdapter(old_api)
translator = Translator(new_provider)  # Works seamlessly!
```

## Composition Over Inheritance

Always prefer composition to inheritance.

```python
# ❌ Bad: Deep inheritance hierarchy
class BaseLLM:
    pass

class ProviderWithCaching(BaseLLM):
    pass

class ProviderWithLogging(ProviderWithCaching):
    pass

class ProviderWithRetry(ProviderWithLogging):
    pass

# ✓ Good: Composition with decorators
def with_caching(provider: BaseLLMProvider) -> BaseLLMProvider:
    """Add caching to any provider."""
    cache = {}
    
    def generate_cached(prompt: str, config: LLMConfig | None = None) -> LLMResponse:
        key = f"{prompt}:{config}"
        if key in cache:
            return cache[key]
        result = provider.generate(prompt, config)
        cache[key] = result
        return result
    
    # Return modified provider
    class CachedProvider:
        @property
        def name(self) -> str:
            return provider.name
        
        def generate(self, prompt: str, config: LLMConfig | None = None) -> LLMResponse:
            return generate_cached(prompt, config)
    
    return CachedProvider()

# Usage: Stack behaviors
provider = ProviderFactory.create_default()
provider = with_caching(provider)  # Add caching
provider = with_logging(provider)  # Add logging
provider = with_retry(provider)    # Add retry
```

## Decision Tree: Which Pattern?

```
Do you need different implementations?
  ├─ Yes, for the same interface → Use Factory
  │
  ├─ Yes, swappable algorithms → Use Strategy
  │
  └─ Need to route to different handlers? → Use Router

Need to handle errors gracefully?
  └─ Yes → Use Error Handling Chain

Need to combine multiple behaviors?
  └─ Yes → Use Composition/Decorators

Need to adapt old code?
  └─ Yes → Use Adapter
```

## Summary

| Pattern | Use When | Example |
|---------|----------|---------|
| Factory | Create objects without specifying classes | `ProviderFactory.create()` |
| Strategy | Swap algorithms at runtime | `DirectTranslation` vs `BackTranslation` |
| Router | Route to different handlers | `FeatureRouter.route(Feature.TRANSLATE)` |
| Error Chain | Handle errors with fallbacks | Try Claude, fallback to GPT |
| Adapter | Bridge incompatible interfaces | Wrap legacy API in new interface |
| Composition | Combine behaviors | Stack decorators (caching → logging → retry) |

## References

- [Design Patterns (Gang of Four)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Python Patterns](https://python-patterns.guide/)
- [Composition over Inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance)
