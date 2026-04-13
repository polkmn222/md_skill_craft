# Claude Code Trainer - Learning & Practice Guide

This project is a **tool for learning how to set up projects using Claude Code** and practicing the process.

## 🎯 Goal

When a new project comes in, develop the ability to **create appropriate CLAUDE.md and Skills for that specific project**.

---

## 📋 Practice Workflow

### Phase 1: Project Analysis (15 minutes)

When given a new project folder:

```bash
# Understand project structure
find <PROJECT> -type f -name "*.md" | head -20
find <PROJECT> -type f -name "package.json" -o -name "pyproject.toml" -o -name "Dockerfile"

# Read README
cat <PROJECT>/README.md

# Check core files
ls -la <PROJECT>/src  # or main code directory
cat <PROJECT>/package.json  # or requirements.txt

# Check existing configuration
cat <PROJECT>/CLAUDE.md  # if it exists
```

**Questions to answer through analysis:**
- [ ] Programming language (Python, TypeScript, Go, Rust, etc.)
- [ ] Project type (Web App, CLI Tool, Game, Library, etc.)
- [ ] Core framework/library
- [ ] Project scale (small, medium, large)
- [ ] Team or solo development?
- [ ] Already established rules/patterns?

### Phase 2: Template Selection (5 minutes)

Choose the **CLAUDE.md template** based on project type:

```
skills/templates/
├── TEMPLATE_PYTHON_WEB.md       # Django, Flask, FastAPI
├── TEMPLATE_PYTHON_CLI.md        # Click, Typer, argparse
├── TEMPLATE_TYPESCRIPT_WEB.md    # Next.js, Vue, React
├── TEMPLATE_TYPESCRIPT_GAME.md   # Phaser, Three.js
├── TEMPLATE_GO_API.md            # Gin, Echo
├── TEMPLATE_RUST_CLI.md          # Clap, Structopt
└── TEMPLATE_SELECTION_GUIDE.md   # Template selection guide
```

### Phase 3: Write CLAUDE.md (20 minutes)

Customize the selected template for your project:

```markdown
# MyProject

## Project
[One-line project description]
**Stack**: [Main technologies]

## Key Commands
| Task | Command |
|------|---------|
| [Main task] | [Actual command] |

## Architecture
- `src/` - [Role]
- `tests/` - [Role]

## Conventions
- [Core rule 1]
- [Core rule 2]

## Skills
@skills/... @skills/...
```

**Sections to customize:**
1. "Project" - project description
2. "Key Commands" - actual commands for your project
3. "Architecture" - directory structure
4. "Conventions" - project rules
5. "Skills" - relevant skills references

### Phase 4: Customize Skills (30 minutes)

Adapt existing skills for your project:

**Mapping Guide:**

| Skill | Adapt for | How to Adapt |
|-------|-----------|-------------|
| `coding-standards.md` | Language/style section | Change language (Python → TypeScript) |
| `validation.md` | Tools section | Replace tools (ruff → eslint, pytest → vitest) |
| `orchestration.md` | Code examples | Replace with your project patterns |
| `memory.md` | General advice | Usable as-is |
| `harness.md` | Reference | No changes needed |
| `hooks.md` | Examples | Adapt to project-specific risks |

**Example: Adapting to Python project**

```markdown
# Original (TypeScript)
```bash
eslint app/
npx tsc --noEmit
vitest tests/
```

# Adapted (Python)
```bash
ruff check src/
mypy src/
pytest tests/
```
```

---

## 🎓 Learning Levels

### Level 1️⃣: Simple CLI Project
- Minimal dependencies
- Simple commands
- Minimal customization

**Practice:** Create CLAUDE.md for Python CLI project

### Level 2️⃣: Web/App Project
- Multiple directory structure
- Build process included
- Testing framework required

**Practice:** Apply Skills to TypeScript Web project

### Level 3️⃣: Complex Project
- Monorepo structure
- Multiple languages
- Special workflows

**Practice:** Optimize existing project (like H1)

---

## 📝 Template Customization Checklist

```markdown
# CLAUDE.md Customization Checklist

## Basic Info
- [ ] Project name changed?
- [ ] One-line description added?
- [ ] Stack information accurate?

## Key Commands
- [ ] Do all commands work in your project?
- [ ] Development server start command?
- [ ] Test command?
- [ ] Build command?

## Architecture
- [ ] Matches actual directory structure?
- [ ] Is each folder's role clear?

## Conventions
- [ ] Are core project rules included?
- [ ] Anti-patterns listed?
- [ ] Type hinting/linting tools correct?

## Skills
- [ ] Reference only necessary skills?
- [ ] Remove unnecessary skills?
- [ ] Add specialized skills (games, web, etc.)?
```

## 💡 Skill Adaptation Patterns

### Pattern 1: Language Conversion

```markdown
# Find: All examples starting with "Python"
# Replace: Convert to TypeScript/JavaScript

# Example
## Before (validation.md in Python context)
```python
pytest tests/
mypy app/
```

## After (validation.md in TypeScript context)
```bash
vitest tests/
npx tsc --noEmit
```
```

### Pattern 2: Tool Replacement

```markdown
# Create a tool mapping table

| Function | Python | TypeScript | Go |
|----------|--------|------------|-----|
| Linter | ruff | eslint | golangci-lint |
| Type Check | mypy | tsc | (built-in) |
| Test | pytest | vitest | go test |
| Format | ruff format | prettier | gofmt |
| Build | pip | npm build | go build |
```

### Pattern 3: Add Project-Specific Skills

```markdown
# Create specialized skills for your project

Example: H1 game project
- Existing: coding-standards.md (general TypeScript)
- Add: phaser-patterns.md (game-specific)
- Add: typing-for-games.md (game type safety)

Example: Django project
- Existing: coding-standards.md (general Python)
- Add: django-patterns.md (Django patterns)
- Add: django-testing.md (Django testing)
```

---

## 🚀 Real Practice Scenarios

### Scenario 1: Analyze New Project

```
User: "Look at this file and create CLAUDE.md"
Claude Code Trainer:
1. Analyze files (read project structure)
2. Determine project type
3. Suggest appropriate template
4. Explain customization needed
5. Present final CLAUDE.md
```

### Scenario 2: Customize Existing Skills

```
User: "Can you adapt coding-standards.md for this project?"
Claude Code Trainer:
1. Analyze project language/characteristics
2. Show needed changes
3. Compare Before/After
4. Present final adapted file
```

### Scenario 3: Create Specialized Skill

```
User: "This is a game project. What skills should I add?"
Claude Code Trainer:
1. Analyze project characteristics
2. Suggest specialized skill (e.g., phaser-patterns.md)
3. Guide on required content
4. Generate final skill file
```

---

## 📚 Reference Materials

- `README.md` - Claude Code Trainer overview
- `CLAUDE.md` - This project's own CLAUDE.md
- `FOUNDATION_GUIDE.md` - Check skills exist and assess project fit
- `QUICK_START.md` - Step-by-step quick guide
- `skills/` - Reusable foundation skills
- `skills/templates/` - Templates for different project types

---

## 🎯 Final Goals

After completing this guide:

✅ Create **CLAUDE.md in 15 minutes** for a new project  
✅ **Customize existing skills** for any project type  
✅ **Write project-specific skills** (games, web, CLI, etc.)  
✅ **Optimize your own projects** with Claude Code

---

**Ready to practice!** 🚀

In `/Users/sangyeol.park@gruve.ai/Documents/Claude Code Trainer`:
- Explore templates for different project types
- Study H1 project customization as example
- Practice with new projects
