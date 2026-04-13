# Foundation Guide: Claude Code Trainer

This guide helps you understand what Claude Code Trainer is, verify the required skills files exist, and assess if your project is suitable for the training.

---

## 📋 Checklist: Required Skills Files

Before starting, verify all **6 foundation skills** are present in `skills/` directory:

```bash
# Check if all files exist
ls -1 skills/ | grep -E "(harness|coding-standards|validation|orchestration|memory|hooks)"
```

### ✅ Required Files

| File | Purpose | Status |
|------|---------|--------|
| `harness.md` | Claude Code structure, CLAUDE.md vs Skills | ✅ |
| `coding-standards.md` | Code style, naming conventions, type hints | ✅ |
| `validation.md` | Testing, linting, type checking strategies | ✅ |
| `orchestration.md` | Design patterns (Factory, Strategy, Router) | ✅ |
| `memory.md` | Context management, token optimization | ✅ |
| `hooks.md` | Claude Code automation via settings.json | ✅ |

**If any file is missing:**
```bash
# Restore from backup or recreate
cp BACKUP_LOCATION/skills/*.md skills/
```

---

## 🎯 Is Your Project Suitable?

### ✅ SUITABLE Projects

Your project is **good for Claude Code Trainer** if it has:

- [ ] Clear project structure (src/, tests/, docs/)
- [ ] Defined conventions (linting, formatting, testing)
- [ ] Build/run process (scripts, makefiles, npm)
- [ ] Test suite (pytest, vitest, jest, go test)
- [ ] Type system (Python typing, TypeScript, Go, Rust)
- [ ] Documentation (README, architecture docs)
- [ ] Multiple developers or planned collaboration

**Examples:**
- ✅ FastAPI web application
- ✅ Next.js frontend
- ✅ Go microservice
- ✅ Rust CLI tool
- ✅ Phaser 3 game (H1)
- ✅ Django backend

### ❌ NOT SUITABLE Projects

Your project is **not ideal** if it's:

- [ ] Minimal scripts with no structure
- [ ] No testing framework
- [ ] No type system (untyped Python/JavaScript)
- [ ] No clear conventions
- [ ] Solo hobby project with no documentation
- [ ] Prototype/POC without established patterns

**Examples:**
- ❌ Single Python script
- ❌ Notebook-only data analysis
- ❌ Untyped JavaScript files
- ❌ No tests or CI/CD

---

## 🚀 Step 1: Analyze Your Project

### 1.1 Project Structure
```bash
# View directory structure
tree -L 2 <PROJECT>
# or
find <PROJECT> -maxdepth 2 -type d
```

**Questions to answer:**
- [ ] What's the main language? (Python, TypeScript, Go, Rust)
- [ ] What's the project type? (Web, CLI, Game, Library, Data)
- [ ] What's the main framework? (FastAPI, Next.js, Phaser, Gin)
- [ ] How many directories? (simple vs complex)

### 1.2 Check for Existing Standards
```bash
# Look for existing config files
ls -la <PROJECT> | grep -E "(\.md|\.json|\.toml|\.yaml|\.cfg)"

# Check package files
cat <PROJECT>/package.json  # npm/yarn/pnpm
cat <PROJECT>/pyproject.toml  # Python
cat <PROJECT>/go.mod  # Go
cat <PROJECT>/Cargo.toml  # Rust
```

**Questions to answer:**
- [ ] Does a README exist? (content quality?)
- [ ] Are linting/formatting tools configured? (ruff, eslint, go fmt)
- [ ] Is there a test framework? (pytest, vitest, jest, go test)
- [ ] Type checking enabled? (mypy, tsc, govet, clippy)

### 1.3 Review README
```bash
cat <PROJECT>/README.md
```

**Look for:**
- [ ] Clear project description
- [ ] Setup instructions
- [ ] Development workflow
- [ ] Key commands (test, lint, build)
- [ ] Architecture overview

---

## 🔍 Step 2: Assess Project Fit

### Scoring Rubric

**Score each category 0-2 points:**

#### Code Standards (0-2)
- 0: No conventions, inconsistent style
- 1: Some conventions, partial typing
- 2: Clear conventions, type hints throughout

#### Testing (0-2)
- 0: No tests
- 1: Some tests, low coverage
- 2: Comprehensive tests, CI/CD configured

#### Documentation (0-2)
- 0: No docs
- 1: Basic README only
- 2: README + architecture docs + code comments

#### Structure (0-2)
- 0: Single directory, all files mixed
- 1: Some organization (src/, tests/)
- 2: Clear structure (src/, tests/, docs/, scripts/)

#### Build/Run (0-2)
- 0: Manual setup, unclear commands
- 1: Some scripts, partially automated
- 2: Clear Makefile/scripts, one-command setup

**Total Score: 0-10**

**Interpretation:**
- 8-10: **Excellent** - Ready for Claude Code optimization
- 6-7: **Good** - Worth applying Claude Code
- 4-5: **Fair** - Needs some cleanup first
- 0-3: **Poor** - Focus on basics before Claude Code

---

## 📚 Step 3: Which Skills Do You Need?

Not all projects need all 6 skills. Use this guide to pick what's relevant:

### 1. `harness.md` - ALWAYS READ
**Required for:** Everyone
**Why:** Explains Claude Code structure and how to use CLAUDE.md + Skills

**When to skip:** Never

---

### 2. `coding-standards.md` - Almost Always
**Required for:** Projects with code (not data-only)

**Read if:**
- [ ] Need to establish code style
- [ ] Want to improve code quality
- [ ] Adding new contributors

**Skip if:**
- Project is data/notebook only
- Already has strict style guide elsewhere

---

### 3. `validation.md` - Highly Recommended
**Required for:** Projects with tests

**Read if:**
- [ ] Setting up testing framework
- [ ] Want CI/CD validation strategy
- [ ] Need linting/type-checking

**Skip if:**
- No testing currently planned
- Tests already well-established

---

### 4. `orchestration.md` - If Using Patterns
**Required for:** Complex projects with multiple modules

**Read if:**
- [ ] Building Factory, Strategy, Router patterns
- [ ] Need provider abstraction (like Claude Code Trainer)
- [ ] Multiple independent components

**Skip if:**
- Simple monolithic application
- Already using design patterns elsewhere

---

### 5. `memory.md` - Optional, Context-Specific
**Required for:** LLM-heavy applications

**Read if:**
- [ ] Building with Claude/GPT/Gemini APIs
- [ ] Managing large context windows
- [ ] Need token optimization

**Skip if:**
- Not using LLM APIs
- Simple single-request flows

---

### 6. `hooks.md` - Power Users
**Required for:** Automation enthusiasts

**Read if:**
- [ ] Want to automate validation with hooks
- [ ] Need git/tool integration
- [ ] Enforcing security checks

**Skip if:**
- Happy with manual validation
- CI/CD already handles checks

---

## 🎓 Step 4: Create Your Checklist

Use this template for your project:

```markdown
# <PROJECT_NAME> Claude Code Assessment

## Project Info
- Language: [Python / TypeScript / Go / Rust]
- Type: [Web / CLI / Game / Library / Data]
- Framework: [FastAPI / Next.js / Phaser / etc.]

## Structure Score: [0-2]
- [ ] Clear separation (src/, tests/, docs/)
- [ ] Consistent naming conventions
- [ ] Comments/documentation

## Code Standards Score: [0-2]
- [ ] Type hints (if applicable)
- [ ] Linting configured (ruff, eslint, go fmt)
- [ ] Code style enforced

## Testing Score: [0-2]
- [ ] Test framework present (pytest, vitest, go test)
- [ ] Tests run in CI
- [ ] Coverage > 50%

## Documentation Score: [0-2]
- [ ] README explains setup
- [ ] Architecture documented
- [ ] API/examples provided

## Build/Run Score: [0-2]
- [ ] One-command setup (make, npm, cargo)
- [ ] Clear dev workflow
- [ ] Deployment automated

## Total Score: [0-10]

## Skills Assessment
- [ ] Read `harness.md` (required)
- [ ] Read `coding-standards.md` (language-specific)
- [ ] Read `validation.md` (testing strategy)
- [ ] Read `orchestration.md` (if using patterns)
- [ ] Read `memory.md` (if using LLMs)
- [ ] Read `hooks.md` (for automation)

## Next Steps
1. Select appropriate template from `skills/templates/`
2. Create CLAUDE.md based on template
3. Apply relevant skills
4. Customize for your project
```

---

## 🔄 Step 5: Compare With Examples

Look at existing CLAUDE.md files to understand the pattern:

```bash
# Current project (Claude Code Trainer - Prompt Eng App)
cat CLAUDE.md

# Game project example (H1 - Phaser 3 Game)
cat ../Development/H1/CLAUDE.md
```

**Observe:**
- How commands are formatted
- How architecture is documented
- Which skills are referenced
- How conventions are listed

---

## 📖 Foundation Skills Overview

### Quick Summary

| Skill | When | What |
|-------|------|------|
| **harness.md** | Always | Claude Code basics |
| **coding-standards.md** | Code projects | Style + type hints |
| **validation.md** | Testing projects | Test/lint/type strategy |
| **orchestration.md** | Complex projects | Design patterns |
| **memory.md** | LLM projects | Context + tokens |
| **hooks.md** | Power users | Automation |

### Learn Paths

**Path A: Web Developer**
1. `harness.md`
2. `coding-standards.md` (your language)
3. `validation.md`
4. `orchestration.md`

**Path B: Game Developer**
1. `harness.md`
2. `coding-standards.md` (TypeScript)
3. `validation.md`
4. `orchestration.md`
5. `phaser-patterns.md` (project-specific)

**Path C: CLI/Script Developer**
1. `harness.md`
2. `coding-standards.md` (your language)
3. `validation.md`

**Path D: LLM Application**
1. `harness.md`
2. `coding-standards.md`
3. `memory.md`
4. `orchestration.md`

---

## ✅ Completion Checklist

- [ ] Read this Foundation Guide
- [ ] Verified all 6 skills files exist
- [ ] Analyzed your project (Step 1)
- [ ] Assessed project fit (Step 2)
- [ ] Identified needed skills (Step 3)
- [ ] Created project checklist (Step 4)
- [ ] Reviewed example CLAUDE.md files (Step 5)

**Next:** Follow `QUICK_START.md` or `TRAINING_GUIDE.md`

---

## 🆘 Troubleshooting

**Q: Some skills files are missing**
```bash
# Check git status
git status skills/

# Restore from main branch
git checkout main -- skills/
```

**Q: Project doesn't fit any template**
```bash
# Use closest match
# Python + custom → TEMPLATE_PYTHON_WEB.md
# TypeScript + custom → TEMPLATE_TYPESCRIPT_WEB.md
# Then customize heavily
```

**Q: Should I read all 6 skills?**
```bash
No. Use the assessment above to pick 3-4 most relevant.
Start with harness.md (always).
Then your language/type specific skill.
Then testing/validation skill.
```

---

**Ready to start? Read `QUICK_START.md` next!** 🚀
