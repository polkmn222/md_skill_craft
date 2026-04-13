# CLAUDE.md Sample

> Example configuration file for Claude API projects.
> This is how you should structure it.

---

# md-skill-craft

## Project
Interactive CLI tool for generating and validating LLM-specific configuration files (CLAUDE.md, AGENT.md, GEMINI.md).
Supported LLMs: Claude (Anthropic), GPT (OpenAI), Gemini (Google).
**Python 3.12+** with type hints (mypy strict mode).

## Setup
1. `pip install -e .` or `pip install -r requirements.txt`
2. Run: `md-skill-craft` (opens interactive REPL)
3. First run: automatic onboarding (language, LLM, API key setup)

## Key Commands

**In REPL:**
| Task           | Command      | Notes |
|----------------|--------------|-------|
| Help           | `/help`      | Show available commands |
| Settings       | `/setup`     | Change language, LLM, mode, API key |
| Cost Tracking  | `/cost`      | Display API usage and estimated costs |
| Mode Toggle    | `/mode`      | Switch between Mode 1 (generate) and Mode 2 (analyze) |
| Exit           | `/exit`      | Quit the program |

**Dev Commands:**
| Task       | Command                  |
|------------|--------------------------|
| Lint       | `ruff check src/`        |
| Format     | `ruff format src/`       |
| Typecheck  | `mypy src/`              |
| Test       | `pytest tests/ -v`       |

## Architecture
- `src/md_skill_craft/` — Main package
  - `cli.py` — REPL loop + /command dispatch
  - `core/` — LLM provider abstraction (Protocol + 3 implementations)
  - `modes/`
    - `mode1_guide.py` — Interactive guide generation
    - `mode2_analysis.py` — Project analysis & validation
  - `config/`
    - `settings.py` — Config management (platformdirs)
    - `keystore.py` — API key storage (keyring)
    - `pricing.py` — LLM pricing & cost calculation
  - `ui/`
    - `menu.py` — Interactive menus (Rich)
    - `progress.py` — Progress bars (Rich)
    - `formatter.py` — Terminal formatting (Rich)
- `skills/` — Reusable documentation and templates
- `tests/` — Unit test suite (58 tests)

## Conventions
- Type hints required on all functions (mypy strict)
- Google-style docstrings
- Never commit `.env` or `.env.local`
- All LLM providers implement BaseLLMProvider protocol
- Use `match` statements (Python 3.12+) for dispatch
- Bilingual support (Korean/English) in all user-facing strings
- Rich library for terminal UI

## Configuration
**API Keys:** Stored in OS keychain (macOS Keychain, Windows Credential Manager, Linux libsecret)
**Settings:** `~/.config/md-skill-craft/config.json` (platformdirs)
**Usage Tracking:** `~/.config/md-skill-craft/usage.json`

**Environment Variables (optional):**
- `ANTHROPIC_API_KEY` — Claude API key
- `OPENAI_API_KEY` — OpenAI API key
- `GOOGLE_API_KEY` — Gemini API key

## Dependencies
See `pyproject.toml` [project.dependencies]:
- `rich` — Terminal UI (menus, progress, formatting)
- `keyring` — OS keychain integration
- `platformdirs` — Cross-platform config paths

Dev: `pytest`, `pytest-asyncio`, `pytest-mock`, `ruff`, `mypy`

## Skills
See `@skills/harness.md` for development workflow and `@skills/coding-standards.md` for code style guidelines.
