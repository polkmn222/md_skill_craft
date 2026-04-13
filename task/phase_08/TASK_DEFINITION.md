# Phase 8: Packaging & Final Cleanup

## Overview
Finalize the md-skill-craft project by removing legacy code, updating documentation, and preparing for distribution.

## Task Definition

### What to implement
1. **Remove Legacy Code**
   - Delete old `app/` directory (was replaced by `src/md_skill_craft/`)
   - Delete `app/main.py` (CLI replaced by new cli.py)
   - Delete `app/web_ui.py` (Web UI removed entirely)
   - Keep only core providers if referenced elsewhere

2. **Update CLAUDE.md**
   - Update to reflect CLI-only design
   - Update setup instructions for CLI
   - Update Key Commands section
   - Update Architecture section
   - Reference Mode 1 and Mode 2

3. **Update README.md**
   - Project overview
   - Installation instructions
   - Quick start guide
   - Feature list
   - Development setup

4. **Generate requirements.txt**
   - Extract from pyproject.toml
   - Include all dependencies and dev dependencies

5. **Verify Installation**
   - Test pip install -e .
   - Verify md-skill-craft command works
   - Run all tests

### Files to Create/Modify
- ✅ Delete: `app/` directory
- ✅ Delete: `web_ui.py` if exists
- ✅ Modify: `CLAUDE.md`
- ✅ Modify: `README.md`
- ✅ Create/Update: `requirements.txt`
- ✅ Verify: `pyproject.toml` (already updated)

### Testing Requirements
- All 82 unit tests pass (Mode 1: 20, Mode 2: 24, CLI: 16, Plus existing tests)
- CLI commands work (/help, /setup, /cost, /mode, /exit)
- Mode 1 and Mode 2 workflows complete successfully (with mocked LLM)

### Success Criteria
- [x] No more `app/` directory with old code
- [x] CLAUDE.md updated for CLI design
- [x] README.md updated with new structure
- [x] requirements.txt generated from pyproject.toml
- [x] All tests pass
- [x] `pip install -e .` works
- [x] `md-skill-craft` command is available
