# CLAUDE.md Template Selection Guide

Choose the appropriate template based on your project type.

## 🐍 Python Projects

### `TEMPLATE_PYTHON_WEB.md`
**For**: Django, FastAPI, Flask web applications
- REST API servers
- Database integration
- Database migrations, model definitions

**Features**:
- `make` or `poetry` commands
- `pytest` testing
- `ruff`, `mypy` linting/type checking
- Database migrations

**Examples**: Blog API, e-commerce backend

### `TEMPLATE_PYTHON_CLI.md`
**For**: Click, Typer, argparse CLI tools
- Command-line utilities
- Data processing scripts
- Batch jobs

**Features**:
- `python -m` execution
- Environment variable configuration
- Simple testing with pytest
- Pip/setuptools distribution

**Examples**: File conversion tool, deployment script

---

## 📘 TypeScript/JavaScript Projects

### `TEMPLATE_TYPESCRIPT_WEB.md`
**For**: Next.js, React, Vue, Svelte web applications
- Full-stack web apps
- SPA (Single Page Application)
- Frontend-only projects

**Features**:
- Vite/Next.js build tools
- `npm` scripts
- `vitest`/`jest` testing
- `eslint`, `prettier` code quality

**Examples**: SaaS dashboard, e-commerce website

### `TEMPLATE_TYPESCRIPT_GAME.md`
**For**: Phaser, Three.js, Babylon.js games
- Browser-based games
- 3D/2D graphics
- Game engine architecture

**Features**:
- Vite development server
- Scene-based architecture
- Game logic testing
- Canvas or WebGL rendering

**Examples**: Turn-based game (like H1), real-time multiplayer game

---

## 🔵 Go Projects

### `TEMPLATE_GO_API.md`
**For**: Gin, Echo, Chi REST APIs
- Backend services
- Microservices
- API servers

**Features**:
- `go run ./cmd/...` execution
- Docker support
- `go test` testing
- Environment configuration management

**Examples**: REST API, gRPC service, microservice

---

## 🦀 Rust Projects

### `TEMPLATE_RUST_CLI.md`
**For**: Clap, Structopt CLI tools
- System utilities
- Performance-critical applications
- Command-line tools

**Features**:
- `cargo` build system
- Strict type checking
- Performance optimizations (LTO, codegen units)
- Cross-compilation

**Examples**: File processor, system utility

---

## 🎯 Selection Criteria

```
What is your project's core purpose?
├─ Web server → PYTHON_WEB / GO_API / TYPESCRIPT_WEB
├─ CLI tool → PYTHON_CLI / RUST_CLI
├─ Game/graphics → TYPESCRIPT_GAME
└─ Other → Choose most similar template
```

## 📝 How to Use

### Step 1: Choose Template
```bash
# Example: Python FastAPI project
cat skills/templates/TEMPLATE_PYTHON_WEB.md
```

### Step 2: Copy and Customize for Your Project
```bash
# Copy to your project folder
cp skills/templates/TEMPLATE_PYTHON_WEB.md <YOUR_PROJECT>/CLAUDE.md

# Edit with your project information:
# - Project name
# - Stack details
# - Key commands
# - Architecture overview
# - Conventions
```

### Step 3: Apply Skills
```bash
# Copy reusable skills to your project
cp -r skills/ <YOUR_PROJECT>/

# Remove skills not relevant to your project
rm <YOUR_PROJECT>/skills/phaser-patterns.md  # if not a game
```

## 🔧 Customization Example

### Before (Template)
```markdown
# [PROJECT_NAME]

## Project
[One-line project description]
**Stack**: FastAPI, PostgreSQL, Python 3.11
```

### After (Customized)
```markdown
# BlogAPI

## Project
REST API for a blogging platform with user authentication, posts, and comments.
**Stack**: FastAPI, PostgreSQL, Python 3.11, Pydantic v2
```

---

## ✅ Complete Template List

| Template | Language | Framework | Use Case |
|----------|----------|-----------|----------|
| TEMPLATE_PYTHON_WEB.md | Python | FastAPI/Django/Flask | REST APIs, Web servers |
| TEMPLATE_PYTHON_CLI.md | Python | Click/Typer | Command-line tools |
| TEMPLATE_TYPESCRIPT_WEB.md | TypeScript | Next.js/React/Vue | Web applications |
| TEMPLATE_TYPESCRIPT_GAME.md | TypeScript | Phaser/Three.js | Browser games |
| TEMPLATE_GO_API.md | Go | Gin/Echo | REST APIs, Microservices |
| TEMPLATE_RUST_CLI.md | Rust | Clap | System utilities |

---

**Ready to create your CLAUDE.md? Pick a template above!** 🚀
