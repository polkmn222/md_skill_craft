# AGENT.md Sample

> Example configuration file for OpenAI GPT projects.
> This is how you should structure it.

---

# [PROJECT_NAME]

## Project
[One-line project description for OpenAI Agents]
Supported: OpenAI GPT models (GPT-4, GPT-4o, etc.)

## Setup
1. Copy `.env.example` → `.env` and add API keys
2. `pip install -r requirements.txt` or `uv sync`
3. Run: [setup command based on project]

## Key Commands
| Task       | Command                    |
|------------|----------------------------|
| Dev        | [development command]      |
| Test       | `pytest tests/ -v`         |
| Lint       | `ruff check src/`          |
| Typecheck  | `mypy src/`                |
| Format     | `ruff format src/`         |

## Architecture
- `src/` — Main source code
- `agents/` — OpenAI Agent definitions
- `tools/` — Tool definitions for agents
- `config/` — Configuration management
- `tests/` — Test suite

## Conventions
- Type hints required on all functions
- Google-style docstrings
- Never commit `.env` file
- Agent functions must be pure and testable
- All agents implement defined interface

## Dependencies
See `pyproject.toml` [project.dependencies]. Dev tools: ruff (lint/format), mypy (types), pytest.

## Skills
See `@skills/harness.md` for project setup, `@skills/coding-standards.md` for code guidelines.
