---
name: Claude Code Harness
description: Understanding Claude Code structure, CLAUDE.md, Skills, Hooks, and how they work together
type: reference
---

# Claude Code Harness Guide

Claude Code is the AI-assisted development environment. This guide explains how it works and the three main components that shape its behavior.

## The Three Components

### 1. **CLAUDE.md** (Always Loaded)
- **What**: A single markdown file at project root
- **Size**: 30 lines maximum recommended
- **When loaded**: On every Claude Code session in this project
- **Content**: Project-specific rules, commands, conventions
- **Scope**: Applies to entire project

```markdown
# MyProject

## Key Commands
| Command | What |
|---------|------|
| make build | Build project |

## Conventions
- Use snake_case for files
- Type hints required

## Skills
@skills/testing.md @skills/performance.md
```

**Why 30 lines?** Longer CLAUDE.md files degrade instruction-following quality. Put details in Skills instead.

### 2. **Skills** (Load on Demand)
- **What**: Reusable `.md` files in `skills/` directory
- **When loaded**: Only when explicitly referenced with `@skills/filename.md`
- **Content**: Detailed guidelines, patterns, best practices
- **Scope**: Specific topic (e.g., testing, security)
- **Reusable**: Copy `skills/` across projects

Example reference in CLAUDE.md:
```markdown
## Testing Guidelines
See @skills/testing.md for pytest patterns and fixtures.
```

### 3. **Hooks** (settings.json)
- **What**: Automated scripts triggered by Claude Code events
- **When run**: When you use tools (Bash, Edit, etc.)
- **Content**: Shell scripts (bash/zsh)
- **Scope**: Project-level automation

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "bash scripts/validate-bash.sh"}
        ]
      }
    ]
  }
}
```

## Loading Order

When Claude Code starts a session in your project:

1. **Global CLAUDE.md** (`~/.claude/CLAUDE.md`) — Your personal defaults
2. **Project CLAUDE.md** (`./CLAUDE.md`) — Overrides global settings
3. **Hooks** (`~/.claude/settings.json`) — Activate on tool use
4. **Skills** — Loaded only when referenced (e.g., `@skills/testing.md`)

## CLAUDE.md vs Skills: When to Use Which

| Scenario | Use CLAUDE.md | Use Skills |
|----------|---------------|-----------|
| "Always apply this rule" | ✓ | |
| "Here's an example of the pattern" | | ✓ |
| "Never do X" | ✓ | |
| "Here's 5 examples of how to do X" | | ✓ |
| "Project conventions" | ✓ | |
| "Reuse this across projects" | | ✓ |
| Takes up space (>5 lines) | | ✓ |

## Best Practices

### Keep CLAUDE.md Lean
```markdown
# Bad CLAUDE.md (too much detail)
## Testing
Pytest fixtures use:
- conftest.py for shared fixtures
- @pytest.fixture decorator
- Parametrization with @pytest.mark.parametrize
- Mock objects for external dependencies
... (continues)

# Good CLAUDE.md (delegated to Skills)
## Testing
See @skills/testing.md for pytest patterns, fixtures, mocking.
```

### Reference Skills Explicitly
Don't assume Skills will be found. Always use the `@` syntax:
```markdown
# ✓ Good
See @skills/performance.md for optimization patterns.

# ✗ Bad (ambiguous)
Read the performance guide.
```

### Organize Skills by Topic
```
skills/
├── testing.md       # pytest, mocking, fixtures
├── performance.md   # profiling, caching, algorithms
├── security.md      # auth, secrets, input validation
├── typing.md        # type hints, protocols, generics
└── async.md         # asyncio, concurrency, parallelism
```

## Hooks: When to Use Them

Hooks run **automatically** when you use Claude Code tools. Common use cases:

### Pre-tool Hooks (Validate Before Action)
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "bash scripts/check-bash-safety.sh"}
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {"type": "command", "command": "bash scripts/check-sensitive-files.sh"}
        ]
      }
    ]
  }
}
```

### Post-tool Hooks (Cleanup After Action)
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {"type": "command", "command": "ruff check ${CLAUDE_TOOL_OUTPUT_PATH}"}
        ]
      }
    ]
  }
}
```

**Hooks best practices:**
- Keep hooks fast (<1 second)
- Exit 0 = allow, exit 1 = block
- Use `$CLAUDE_TOOL_INPUT` env var to inspect what Claude is about to do
- Document what the hook does in CLAUDE.md

## Anti-Patterns

❌ **Duplicate info**: Don't put the same guidance in CLAUDE.md and multiple Skills.
- Fix: Put it in one place; reference it from others.

❌ **Overstuffed CLAUDE.md**: Putting detailed examples or code in CLAUDE.md.
- Fix: Move examples to Skills files.

❌ **Silent hooks**: Hooks that block without clear error messages.
- Fix: Echo helpful error output so Claude understands why it failed.

❌ **Unreferenced skills**: Creating skills that nobody links to.
- Fix: Add references to CLAUDE.md or other skills.

## Real-World Example

### Scenario
You're building a FastAPI project and want Claude Code to:
1. Always format code with `black` on edit
2. Only allow `pip install` for dev dependencies
3. Provide detailed testing guidelines

### Solution

**CLAUDE.md** (20 lines)
```markdown
# FastAPI Project

## Stack
- FastAPI, SQLAlchemy, Pytest
- Python 3.11+

## Key Conventions
- Type hints required (mypy strict)
- Docstrings: Google style
- Tests in tests/ parallel to src/

## Testing
See @skills/testing.md for pytest fixtures and patterns.

## Hooks
- Runs `black` on every file edit
- Validates pip commands (dev-only for test deps)
```

**skills/testing.md** (reusable)
```markdown
# Pytest Patterns

## Fixtures (conftest.py)
```python
@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()
```

## Parametrized Tests
```python
@pytest.mark.parametrize("user_id,expected", [(1, "User1"), (2, "User2")])
def test_get_user(user_id, expected):
    assert get_user(user_id).name == expected
```
```

**~/.claude/settings.json** (project hooks)
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {"type": "command", "command": "black ${CLAUDE_TOOL_OUTPUT_PATH}"}
        ]
      }
    ]
  }
}
```

## AI Development Workflow & Process

When working with Claude Code on AI-assisted projects, follow these core principles:

### Work Principles

1. **Explicit Requests Only**
   - Implement only what is explicitly requested
   - Do not expand scope or add features beyond the request
   - Report ambiguous or unclear requirements before proceeding

2. **Accuracy First**
   - Prioritize correctness over speed
   - If something seems suspicious or unclear, report it first rather than fixing it
   - Ask for confirmation before making changes that aren't explicitly requested

3. **Test-Driven Development**
   - Unit tests are mandatory for all code changes
   - Manual testing only when explicitly requested by user
   - Tests verify correctness before deployment

4. **Structured Workflow**
   - Use `Implementation/phase_XX/` for code changes
   - Use `task/phase_XX/` for task definitions and checklists
   - Use `backups/phase_XX/` for backup policies (ask user first)
   - Label each phase clearly in commit messages and documentation

5. **User Confirmation Process**
   - Always show Implementation and task details before proceeding
   - Ask before modifying `.md` files and documentation
   - Report findings and get approval before major structural changes
   - Provide clear summaries when work is complete

### LLM-Specific Configuration

Projects may support multiple LLM tools. Each LLM has its own isolated configuration:

```
project-root/
├── CLAUDE.md          # Claude Code (root level, auto-detected)
├── AGENT.md           # OpenAI Agents (root level, auto-detected)
├── GEMINI.md          # Google Gemini (root level, auto-detected)
│
├── .claude/           # Claude Code specific
│   ├── skills/        # Claude Code reusable guides
│   └── settings.json  # Claude Code hooks & config
│
├── .codex/            # OpenAI Codex/GPT specific
│   ├── skills/        # Codex/GPT reusable guides
│   └── settings.json  # OpenAI configuration
│
└── .gemini/           # Google Gemini specific
    ├── skills/        # Gemini reusable guides
    └── settings.json  # Gemini configuration
```

**How it works:**
- Root `.md` files (CLAUDE.md, AGENT.md, GEMINI.md) are auto-detected by their respective tools
- Each `.md` file references skills from its corresponding LLM-specific directory
- When CLAUDE.md references `@skills/coding-standards.md`, it reads from `.claude/skills/coding-standards.md`
- When AGENT.md references `@skills/coding-standards.md`, it reads from `.codex/skills/coding-standards.md`
- Skills can be identical or LLM-specific depending on project needs

**Example CLAUDE.md reference:**
```markdown
## Code Standards
See @skills/coding-standards.md for guidelines.
# This will load from .claude/skills/coding-standards.md
```

**Example AGENT.md reference:**
```markdown
## Code Standards
See @skills/coding-standards.md for guidelines.
# This will load from .codex/skills/coding-standards.md
```

## Summary

| Component | Where | Size | Reload | Purpose |
|-----------|-------|------|--------|---------|
| CLAUDE.md | Project root | ~30 lines | Every session | Claude Code rules & references |
| AGENT.md | Project root | ~30 lines | Every session | OpenAI Agents rules & references |
| GEMINI.md | Project root | ~30 lines | Every session | Google Gemini rules & references |
| Skills | `.{claude,codex,gemini}/skills/` | Unlimited | On-demand | LLM-specific reusable guidance |
| Hooks | `.{claude,codex,gemini}/settings.json` | Shell scripts | On tool use | Automated validation per LLM |

**The Key Principle**: Root `.md` files say "what" and "why". Skills say "how" with examples. Hooks say "enforce it automatically." Each LLM has isolated configuration.
