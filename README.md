# md-skill-craft

> Interactive CLI for generating and validating LLM-specific project configuration files

Generate **CLAUDE.md**, **AGENT.md**, or **GEMINI.md** for your projects through interactive conversations with Claude, GPT, or Gemini APIs.

## ✨ Features

- **Mode 1: Interactive Guide Generation** — Describe your project, LLM generates configuration file
- **Mode 2: Project Analysis** — Analyze existing code, validate/improve configuration file
- **Multi-LLM Support** — Claude, GPT, Gemini with unified abstraction layer
- **Secure API Key Storage** — OS-level keychain integration (macOS/Windows/Linux)
- **Bilingual** — Korean and English support
- **Cost Tracking** — Monitor API token usage and estimated costs
- **Cross-platform** — Works on macOS, Windows, Linux

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/anthropics/claude-code-trainer
cd claude-code-trainer

# Install
pip install -e .
# or
pip install -r requirements.txt

# Verify
md-skill-craft --version
```

### First Run
```bash
md-skill-craft
```

The CLI opens an interactive REPL with automatic onboarding:
1. **Language** — Choose Korean or English
2. **LLM** — Select Claude, GPT, or Gemini
3. **API Key** — Auto-detect env var or securely store in keychain
4. **Mode** — Choose between generating new configs or analyzing existing projects

### Generate Configuration (Mode 1)
```
md-skill-craft > (press enter)

Describe your project:
> FastAPI REST API with PostgreSQL, deployed on AWS

[LLM analyzes and generates CLAUDE.md]

Options:
  [1] Save to CLAUDE.md
  [2] Save as CLAUDE.md.suggested (preview)
  [3] Continue editing
  [4] Skip
```

### Analyze Project (Mode 2)
```
md-skill-craft > (press enter)

Select analysis depth:
  [1] Fast — README, config files
  [2] Standard — Top-level structure
  [3] Deep — All source files

[LLM scans and validates your existing CLAUDE.md]
```

## 📋 Commands

Within the REPL:

| Command | Description |
|---------|-------------|
| `/help` | Show available commands and current settings |
| `/setup` | Change language, LLM, API key, or mode |
| `/cost` | Display API usage and estimated costs |
| `/mode` | Switch between Mode 1 and Mode 2 |
| `/exit` | Quit the program |

Empty input or text → runs current mode (1 or 2)

## 🏗️ Project Structure

```
md-skill-craft/
├── src/md_skill_craft/
│   ├── cli.py              # REPL loop + command dispatch
│   ├── core/               # LLM provider abstraction
│   │   ├── base_provider.py
│   │   ├── provider_factory.py
│   │   ├── anthropic_provider.py
│   │   ├── openai_provider.py
│   │   └── google_provider.py
│   ├── modes/
│   │   ├── mode1_guide.py  # Interactive guide generation
│   │   └── mode2_analysis.py  # Project analysis
│   ├── config/
│   │   ├── settings.py     # Config management
│   │   ├── keystore.py     # API key storage
│   │   └── pricing.py      # Cost calculation
│   └── ui/                 # Terminal UI (Rich)
├── tests/                  # 82 unit tests
├── skills/                 # Documentation & templates
├── CLAUDE.md              # Project guidelines
└── pyproject.toml         # Package configuration
```

## 🔧 Development

### Setup
```bash
pip install -e ".[dev]"
```

### Tests
```bash
pytest tests/ -v              # Run all tests
pytest tests/test_mode1_guide.py  # Test specific module
pytest tests/test_cli.py -k test_help  # Test specific test
```

### Code Quality
```bash
ruff check src/               # Lint
ruff format src/              # Auto-format
mypy src/                     # Type checking
```

### Build & Release
```bash
pip install build twine
python -m build
twine upload dist/*
```

## 🔐 Configuration

### API Keys
Automatically detected in this order:
1. OS keychain (macOS Keychain, Windows Credential Manager, Linux libsecret)
2. Environment variables: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`
3. User prompt for secure storage

### Config Location
- **macOS/Linux:** `~/.config/md-skill-craft/`
- **Windows:** `C:\Users\<user>\AppData\Roaming\md-skill-craft\`

## 📊 Cost Tracking

Use `/cost` to see API usage:
```
━━━━━━━━━━━━━━━━━━━━━━━━━
📊 API Usage & Cost
━━━━━━━━━━━━━━━━━━━━━━━━━
Claude (claude-haiku-4-5-20251001)
  Input:  45,230 tokens → $0.036
  Output: 12,450 tokens → $0.050
  Subtotal: $0.086

GPT (gpt-4o-mini)
  Input:  23,100 tokens → $0.003
  Output:  5,670 tokens → $0.003
  Subtotal: $0.006
─────────────────────────
Total: $0.092
```

## 🧠 LLM-Specific Config Files

Each LLM has a unique configuration format:

- **CLAUDE.md** — Claude Code project guidelines
- **AGENT.md** — OpenAI Agents configuration
- **GEMINI.md** — Google Gemini project setup

Each file documents:
- Project overview and tech stack
- Setup instructions
- Key commands (dev, test, lint, format, deploy)
- Architecture diagram or description
- Coding conventions
- Dependencies and skills

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Add tests for new functionality
4. Run `ruff check`, `mypy`, and `pytest` locally
5. Commit with clear messages
6. Push and open Pull Request

## 📝 License

MIT License — See LICENSE file for details

## 🔗 Links

- [GitHub Repository](https://github.com/anthropics/claude-code-trainer)
- [Issue Tracker](https://github.com/anthropics/claude-code-trainer/issues)
- [Claude API Docs](https://docs.anthropic.com)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Google Gemini Docs](https://ai.google.dev)

---

**Built with ❤️ by Claude Code**
