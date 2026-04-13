---
name: Memory & Context Management
description: Prompt caching, token management, context windows, conversation history
type: reference
---

# Memory & Context Management

How to efficiently manage LLM context, store conversation history, and handle large inputs.

## Context Windows: What You Have

Each LLM has a maximum context window. Know yours:

| Model | Context | Cost Efficiency |
|-------|---------|-----------------|
| Claude 3 Haiku | 200K tokens | $0.80/$2.40 (1M) |
| Claude 3 Sonnet | 200K tokens | $3/$15 (1M) |
| Claude 3 Opus | 200K tokens | $15/$75 (1M) |
| GPT-4 | 128K tokens | $0.03/$0.06 (1K) |
| GPT-4o | 128K tokens | $0.005/$0.015 (1K) |
| Gemini 1.5 | 1M tokens | $0.075/$0.30 (1M) |

**Tokens vs. Words**: ~4 characters = 1 token, ~1.3 words = 1 token.

## Estimating Token Usage

```python
# Rough estimation (use actual tokenizers for accuracy)
def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token."""
    return len(text) // 4

# For Claude via Anthropic SDK:
from anthropic import Anthropic
client = Anthropic()
messages = [{"role": "user", "content": "Hello"}]
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=100,
    messages=messages,
)
print(f"Input: {response.usage.input_tokens}")
print(f"Output: {response.usage.output_tokens}")
```

## Prompt Caching (Optimization)

Reuse expensive context to save tokens and cost.

```python
# Pattern: Cache system prompts and few-shot examples
SYSTEM_PROMPT = """You are an expert Python developer.
[Long system prompt here]"""

FEW_SHOT_EXAMPLES = """
Example 1:
Input: def add(a, b): ...
Output: Add type hints...

Example 2: ...
[Multiple examples]
"""

# Cache the expensive context
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    system=[
        {
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},  # Cache this block
        },
        {
            "type": "text",
            "text": FEW_SHOT_EXAMPLES,
            "cache_control": {"type": "ephemeral"},
        },
    ],
    messages=[
        {"role": "user", "content": "Review this Python function..."}
    ],
)
```

**Savings**: If system context is cached, future requests save 90% of those tokens.

## Storing Conversation History

For multi-turn interactions, maintain conversation state.

### In-Memory (Simple)

```python
@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str

class Conversation:
    def __init__(self, system_prompt: str = "") -> None:
        self.system = system_prompt
        self.messages: list[Message] = []
    
    def add_user_message(self, content: str) -> None:
        self.messages.append(Message("user", content))
    
    def add_assistant_message(self, content: str) -> None:
        self.messages.append(Message("assistant", content))
    
    def get_history(self) -> list[dict]:
        """Format for API."""
        return [{"role": m.role, "content": m.content} for m in self.messages]
    
    def total_tokens_estimate(self) -> int:
        """Estimate token usage."""
        total = estimate_tokens(self.system)
        for msg in self.messages:
            total += estimate_tokens(msg.content)
        return total

# Usage
conv = Conversation(system_prompt="You are helpful assistant.")
conv.add_user_message("What is AI?")
conv.add_assistant_message("AI is artificial intelligence...")
conv.add_user_message("Give an example.")

# Send to API
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    system=conv.system,
    messages=conv.get_history(),  # Include full history
)
```

### With Gradio State (Web UI)

```python
import gradio as gr

def create_chat_interface():
    # State persists across interactions
    history_state = gr.State(value=[])
    
    def chat(user_message: str, history: list) -> tuple[str, list]:
        """Process user message, return response and updated history."""
        if not user_message:
            return "", history
        
        # Add user message
        history.append({"role": "user", "content": user_message})
        
        # Get response
        provider = ProviderFactory.create_default()
        response = provider.generate(user_message)
        
        # Add assistant response
        history.append({"role": "assistant", "content": response.text})
        
        return response.text, history
    
    with gr.Blocks() as demo:
        chat_display = gr.Chatbot(label="Conversation")
        user_input = gr.Textbox(label="You")
        send_btn = gr.Button("Send")
        
        send_btn.click(
            fn=chat,
            inputs=[user_input, history_state],
            outputs=[chat_display, history_state],
        )
    
    return demo
```

## Chunking Large Inputs

For documents larger than context window, split them.

```python
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks.
    
    Args:
        text: Text to chunk
        chunk_size: Characters per chunk
        overlap: Overlap between chunks (preserves context)
    
    Returns:
        List of text chunks
    """
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    return chunks

# Usage: Process large document
doc = load_large_document()
chunks = chunk_text(doc, chunk_size=2000, overlap=200)

summaries = []
for i, chunk in enumerate(chunks):
    response = provider.generate(f"Summarize:\n{chunk}")
    summaries.append(response.text)
    print(f"Processed chunk {i+1}/{len(chunks)}")

# Combine summaries
final_summary = "\n".join(summaries)
```

## Managing Long Conversations

As conversations grow, token usage increases. Strategies:

### 1. Summarize Old Messages

```python
def summarize_history(
    messages: list[Message],
    keep_last_n: int = 10,
) -> list[Message]:
    """Keep recent messages, summarize old ones."""
    if len(messages) <= keep_last_n:
        return messages
    
    old_messages = messages[:-keep_last_n]
    recent_messages = messages[-keep_last_n:]
    
    # Summarize old messages
    old_text = "\n".join(f"{m.role}: {m.content}" for m in old_messages)
    summary_response = provider.generate(f"Summarize:\n{old_text}")
    
    # Replace with summary
    return [
        Message("system", f"Prior context: {summary_response.text}"),
        *recent_messages,
    ]
```

### 2. Drop Old Messages

```python
def trim_messages(
    messages: list[Message],
    max_tokens: int = 100000,
) -> list[Message]:
    """Keep messages until token limit, drop oldest first."""
    total_tokens = 0
    kept_messages = []
    
    for msg in reversed(messages):  # Start from recent
        tokens = estimate_tokens(msg.content)
        if total_tokens + tokens <= max_tokens:
            kept_messages.append(msg)
            total_tokens += tokens
        else:
            break
    
    return list(reversed(kept_messages))
```

### 3. Separate Context Tiers

```python
# Tier 1: Critical (always included)
critical_context = "System prompt, current task, key facts"

# Tier 2: Recent (last few turns)
recent_messages = conversation.messages[-5:]

# Tier 3: Historical (summarized)
historical_summary = "Earlier conversation: ... (summarized)"

# Build messages
final_messages = [
    {"role": "system", "content": critical_context},
    {"role": "system", "content": historical_summary},
    *[{"role": m.role, "content": m.content} for m in recent_messages],
]

response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    messages=final_messages,
)
```

## Token Counting (Accurate)

Use the SDK's built-in tokenizers when available.

```python
# Anthropic SDK (Claude)
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello!"}],
)

# Check actual usage
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")

# OpenAI (GPT)
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
tokens = enc.encode("Hello, world!")
print(f"Tokens: {len(tokens)}")

# Google (Gemini)
# google-genai SDK has limited token counting
# Estimate or use: 1 token ≈ 4 characters
```

## Caching Strategies

| Strategy | Use Case | Savings |
|----------|----------|---------|
| **System Prompt Cache** | Repeated queries with same system context | 90% system tokens |
| **Few-Shot Cache** | Repeated similar tasks | 70% context tokens |
| **Conversation Summary** | Long multi-turn chats | 80% old message tokens |
| **Chunk Caching** | Document processing | 50% per chunk |

## Monitoring Token Usage

```python
class TokenTracker:
    """Track token usage across requests."""
    
    def __init__(self) -> None:
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_cost = 0.0
    
    def record(self, response: LLMResponse, cost_per_1k: dict) -> None:
        """Record response tokens and cost."""
        self.input_tokens += response.input_tokens
        self.output_tokens += response.output_tokens
        
        # Calculate cost
        input_cost = (response.input_tokens / 1000) * cost_per_1k["input"]
        output_cost = (response.output_tokens / 1000) * cost_per_1k["output"]
        self.total_cost += input_cost + output_cost
    
    def report(self) -> str:
        """Generate usage report."""
        return f"""
Token Usage Report:
- Input: {self.input_tokens:,} tokens
- Output: {self.output_tokens:,} tokens
- Total: {self.input_tokens + self.output_tokens:,} tokens
- Estimated Cost: ${self.total_cost:.2f}
"""

# Usage
tracker = TokenTracker()
response = provider.generate("Hello")
tracker.record(response, cost_per_1k={"input": 0.003, "output": 0.006})
print(tracker.report())
```

## Best Practices

1. **Estimate token usage before API calls** — Avoid surprises
2. **Cache expensive context** — System prompts, few-shot examples
3. **Trim old conversations** — Keep them fresh and relevant
4. **Monitor costs** — Track tokens and spending
5. **Batch requests** — Fewer API calls = lower costs
6. **Use cheaper models for cheap tasks** — Not everything needs GPT-4
7. **Know your limits** — Stay under context window

## References

- [Claude Token Counting](https://docs.anthropic.com/)
- [OpenAI Token Counting](https://platform.openai.com/docs/guides/tokens)
- [Google Gemini Context Windows](https://ai.google.dev/models)
