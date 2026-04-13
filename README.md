# md-skill-craft

> Auto-generate project configuration files with LLMs

**Mode 1:** Project description → Auto-generate CLAUDE.md / AGENT.md / GEMINI.md  
**Mode 2:** Analyze existing projects → Validate and improve configuration files

---

## 🚀 Installation

Choose the LLM provider you want to use:

### 1️⃣ Claude (Anthropic)
```bash
git clone https://github.com/polkmn222/md_skill_craft.git
cd md_skill_craft
bash setup.sh  # macOS/Linux
# or setup.bat  # Windows

pip install -e ".[claude]"
md-skill-craft
```

### 2️⃣ OpenAI (GPT)
```bash
cd md_skill_craft
bash setup.sh

pip install -e ".[openai]"
md-skill-craft
```

### 3️⃣ Google Gemini
```bash
cd md_skill_craft
bash setup.sh

pip install -e ".[gemini]"
md-skill-craft
```

### 4️⃣ All LLM Providers (Claude + OpenAI + Gemini)
```bash
cd md_skill_craft
bash setup.sh

pip install -e ".[all]"
md-skill-craft
```

---

## 📋 Commands

Available in the REPL:

| Command | Description |
|---------|-------------|
| `/help` | Show help and current settings |
| `/setup` | Change settings (language, LLM, API key, mode) |
| `/cost` | Display API usage and costs |
| `/mode` | Switch between Mode 1 and Mode 2 |
| `/exit` | Exit the program |

---

## 🎯 Usage Examples

### Mode 1: Generate Configuration Files
```
md-skill-craft > (press enter)

Describe your project:
> FastAPI REST API with PostgreSQL database

[LLM generates CLAUDE.md automatically]

Save?
  [1] Save to CLAUDE.md
  [2] Save as CLAUDE.md.suggested (preview)
  [3] Continue editing
  [4] Skip
```

### Mode 2: Analyze Existing Projects
```
md-skill-craft > (press enter)

Select analysis depth:
  [1] Fast — README and config files only
  [2] Standard — Top-level source structure
  [3] Deep — All source files

[LLM validates existing CLAUDE.md and suggests improvements]
```

---

## 📁 Project Structure

```
md_skill_craft/
├── src/md_skill_craft/     # Core application code
│   ├── cli.py              # REPL loop and command dispatcher
│   ├── core/               # LLM provider abstraction
│   ├── modes/              # Mode 1 and Mode 2 implementations
│   ├── config/             # Settings and API key management
│   └── ui/                 # Terminal UI components
├── tests/                  # Unit tests (58+ tests)
├── samples/                # Example configuration files
│   ├── CLAUDE.md.sample
│   ├── AGENT.md.sample
│   └── GEMINI.md.sample
├── README.md               # This file
└── pyproject.toml          # Package configuration
```

---

## ⚙️ Development

### Run Tests
```bash
pytest tests/ -v
```

### Code Quality
```bash
ruff check src/          # Lint
ruff format src/         # Format code
mypy src/               # Type checking
```

---

## 🔐 API Key Setup

Auto-detection order:
1. OS Keychain (macOS/Windows/Linux)
2. Environment variables: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`
3. User input (securely stored)

---

## 📝 Sample Configuration Files

See the `samples/` folder for example project configurations:
- `CLAUDE.md.sample` — Claude project example
- `AGENT.md.sample` — OpenAI Agents example
- `GEMINI.md.sample` — Google Gemini example

---

## 🔗 Links

- [GitHub Repository](https://github.com/polkmn222/md_skill_craft)
- [Claude API Documentation](https://docs.anthropic.com)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google Gemini Documentation](https://ai.google.dev)

---

**Requirements:** Python 3.12+
