# 🚀 Claude Code Trainer - Quick Start

## Two Ways to Use

### Method 1️⃣: Prompt Engineering Practice (5 minutes)

```bash
cd "Claude Code Trainer"
python app/web_ui.py
# → Automatically opens http://localhost:7860
```

**3 Features:**
- 🌐 **Translation** - Korean ↔ English practice
- 💡 **Prompt Practice** - Learn 4 techniques (zero-shot, few-shot, chain-of-thought, system role)
- 📝 **Doc Writing** - Auto-generate documentation

**Select Your LLM:**
- 🔴 Claude (Anthropic)
- 🟢 GPT (OpenAI)
- 🔵 Gemini (Google)

---

### Method 2️⃣: Claude Code Training (30 min ~ 2 hours)

Learn how to create CLAUDE.md and Skills for **any new project**.

#### 📋 Learning Steps

**Step 1: Foundation (10 min)**
```bash
cat FOUNDATION_GUIDE.md
```
- Verify all 6 skills files exist
- Assess if your project is suitable
- Determine which skills to read

**Step 2: Project Analysis (15 min)**
```bash
# Understand your project
find <PROJECT> -type f -name "*.md" | head -10
cat <PROJECT>/README.md
cat <PROJECT>/package.json  # or pyproject.toml
```

**Key Questions:**
- What language? (Python, TypeScript, Go, Rust)
- What type? (Web, CLI, Game, Library)
- What framework? (FastAPI, Next.js, Phaser)

**Step 3: Choose Template (5 min)**
```bash
cat skills/templates/TEMPLATE_SELECTION_GUIDE.md
```

Options:
- `TEMPLATE_PYTHON_WEB.md` → FastAPI, Django, Flask
- `TEMPLATE_PYTHON_CLI.md` → Click, Typer
- `TEMPLATE_TYPESCRIPT_WEB.md` → Next.js, React, Vue
- `TEMPLATE_TYPESCRIPT_GAME.md` → Phaser, Three.js
- `TEMPLATE_GO_API.md` → Gin, Echo
- `TEMPLATE_RUST_CLI.md` → Clap, Structopt

**Step 4: Create CLAUDE.md (20 min)**
```bash
# Copy template to your project
cp skills/templates/TEMPLATE_PYTHON_WEB.md <PROJECT>/CLAUDE.md

# Edit these sections:
# - Project name and description
# - Stack information
# - Key commands (dev, test, build, lint)
# - Architecture (directory structure)
# - Conventions (code style, rules)
```

**Step 5: Apply Skills (15 min)**
```bash
# Copy skills to your project
cp -r skills/ <PROJECT>/

# Remove unnecessary skills
rm <PROJECT>/skills/typing-for-games.md  # if not a game

# Reference needed skills in CLAUDE.md
# @skills/coding-standards.md
# @skills/validation.md
# @skills/orchestration.md
```

**Step 6: Create Custom Skills (Optional, 1 hour)**
```bash
# For specialized projects, create project-specific skills
# Example: phaser-patterns.md (already exists for games)
# Example: django-patterns.md (Django-specific)
```

---

## 🎯 Example Walkthrough

### Example: Python FastAPI Project

```bash
# Step 1: Check Foundation
cat FOUNDATION_GUIDE.md
# Score your project (0-10)

# Step 2: Analyze
ls /my-api-project
cat /my-api-project/README.md
cat /my-api-project/requirements.txt

# Step 3: Choose Template
# → Python + Web = TEMPLATE_PYTHON_WEB.md

# Step 4: Create CLAUDE.md
cp skills/templates/TEMPLATE_PYTHON_WEB.md /my-api-project/CLAUDE.md

# Edit the file:
# - Project: "BlogAPI - REST API for blogging platform"
# - Stack: "FastAPI, PostgreSQL, Python 3.11"
# - Commands: "fastapi dev src/main.py"
# - Architecture: "src/api, src/models, src/services, src/db"

# Step 5: Apply Skills
cp -r skills/ /my-api-project/

# Step 6: Done!
cat /my-api-project/CLAUDE.md
```

### Example: TypeScript Game (Phaser)

```bash
# Step 1: Check Foundation
cat FOUNDATION_GUIDE.md

# Step 2: Analyze
cat /my-game/package.json  # Check for Phaser
cat /my-game/src/main.ts

# Step 3: Choose Template
# → TypeScript + Game = TEMPLATE_TYPESCRIPT_GAME.md

# Step 4: Create CLAUDE.md
cp skills/templates/TEMPLATE_TYPESCRIPT_GAME.md /my-game/CLAUDE.md

# Edit:
# - Project: "SpaceShooter - 2D arcade shooter game"
# - Stack: "Phaser 3, TypeScript, Vite"
# - Commands: "npm run dev", "npm test"

# Step 5: Apply Skills
cp -r skills/ /my-game/
# Keep: phaser-patterns.md, typing-for-games.md

# Step 6: Done!
cat /my-game/CLAUDE.md
```

---

## ✅ CLAUDE.md Completion Checklist

```markdown
# Verify Your CLAUDE.md

## Basic Info
- [ ] Project name is correct?
- [ ] One-line description is clear?
- [ ] Stack info is accurate with versions?

## Key Commands
- [ ] All commands work in your project?
- [ ] Dev server startup command?
- [ ] Test command?
- [ ] Build command?
- [ ] Lint command?

## Architecture
- [ ] Matches actual directory structure?
- [ ] Each folder's purpose is clear?

## Conventions
- [ ] Core project rules defined?
- [ ] Anti-patterns listed?
- [ ] Tool configuration correct?

## Skills
- [ ] Only necessary skills referenced?
- [ ] All needed skills included?
- [ ] Skills match your language/framework?

## Final Test
- [ ] Can someone unfamiliar understand the project from this file?
- [ ] Are all commands copy-pasteable?
- [ ] Is the architecture diagram helpful?
```

---

## 📚 Recommended Learning Path

### Beginner (1-2 hours)
1. Read `FOUNDATION_GUIDE.md` (10 min)
2. Read `QUICK_START.md` (this file, 5 min)
3. Analyze a simple project (Python CLI, 15 min)
4. Choose a template (5 min)
5. Write your first CLAUDE.md (30 min)

### Intermediate (2-4 hours)
6. Read `TRAINING_GUIDE.md` (detailed guide, 20 min)
7. Study `harness.md` (Claude Code structure, 30 min)
8. Read `coding-standards.md` (your language, 30 min)
9. Apply skills to a Web project (30 min)
10. Customize skills for your project (30 min)

### Advanced (4+ hours)
11. Read `validation.md` (testing strategy, 30 min)
12. Read `orchestration.md` (design patterns, 30 min)
13. Create project-specific skill (Phaser, Django, etc., 1 hour)
14. Optimize your own project (variable time)

---

## 🔗 File Navigation

```
Claude Code Trainer/
├── FOUNDATION_GUIDE.md ← Start here (check skills, assess project)
├── QUICK_START.md ← This file (step-by-step walkthrough)
├── TRAINING_GUIDE.md ← Detailed explanations
├── README.md ← App features for prompt engineering
├── skills/
│   ├── templates/
│   │   ├── TEMPLATE_SELECTION_GUIDE.md ← Choose template
│   │   ├── TEMPLATE_PYTHON_WEB.md
│   │   ├── TEMPLATE_PYTHON_CLI.md
│   │   ├── TEMPLATE_TYPESCRIPT_WEB.md
│   │   └── TEMPLATE_TYPESCRIPT_GAME.md
│   ├── harness.md ← Claude Code basics (read first)
│   ├── coding-standards.md ← Code style
│   ├── validation.md ← Testing/linting
│   ├── orchestration.md ← Design patterns
│   ├── memory.md ← Context/tokens
│   └── hooks.md ← Automation
└── app/ ← Prompt engineering application
```

---

## ❓ Quick FAQ

**Q: Where do I start?**
```bash
# For prompt engineering practice
python app/web_ui.py

# For learning Claude Code
cat FOUNDATION_GUIDE.md
```

**Q: Which template do I use?**
```bash
cat skills/templates/TEMPLATE_SELECTION_GUIDE.md
# Match your language + project type
```

**Q: How do I know my project fits?**
```bash
cat FOUNDATION_GUIDE.md
# Do the scoring rubric
# 8-10 = Excellent, 6-7 = Good, 4-5 = Fair, 0-3 = Needs work
```

**Q: Do I need to read all 6 skills?**
```bash
No. Read FOUNDATION_GUIDE.md to determine which are relevant.
Always read: harness.md
Also read: 2-3 others based on your project type
```

**Q: How long does this take?**
```bash
Quick: 30 minutes (template → CLAUDE.md)
Complete: 2-3 hours (with skills deep dive)
```

---

## 🎓 Success Criteria

After completing this process:

✅ You can analyze a new project in **15 minutes**  
✅ You can write CLAUDE.md in **20 minutes**  
✅ You can customize skills for your project  
✅ You understand Claude Code structure  
✅ You can optimize your own projects  

---

## 🚀 Ready? Choose Your Path

**Path A: Quick Practice**
```bash
python app/web_ui.py
```

**Path B: Learn Claude Code**
```bash
cat FOUNDATION_GUIDE.md
```

**Path C: Deep Dive**
```bash
cat FOUNDATION_GUIDE.md
cat QUICK_START.md
cat TRAINING_GUIDE.md
```

---

**Let's get started!** 🎯
