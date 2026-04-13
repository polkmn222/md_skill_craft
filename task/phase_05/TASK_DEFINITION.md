# Phase 5: Mode 1 - LLM Interactive Guide Generation

## Overview
Implement Mode 1 functionality: interactive conversation with LLM to generate CLAUDE.md / AGENT.md / GEMINI.md for new projects.

## Task Definition

### What to implement
1. **Mode 1 Guide Generator** (`src/md_skill_craft/modes/mode1_guide.py`)
   - Interactive conversation with user (project description)
   - Multi-turn LLM dialogue for project understanding
   - Template-based file generation
   - Save/Edit/Skip options
   - Generate LLM-specific md files

### Key Features
- **User Input**: Collect project description via conversation
- **LLM Integration**: Multi-turn dialogue with selected LLM provider
- **Template Reference**: Use skills/templates/ for structure
- **File Generation**: Create CLAUDE.md / AGENT.md / GEMINI.md based on LLM choice
- **Output Options**:
  - [1] Save to file
  - [2] Save as .suggested (preview)
  - [3] Continue editing
  - [4] Skip
- **File Locations**:
  - CLAUDE.md → project root
  - AGENT.md → project root
  - GEMINI.md → project root

### Files to Create/Modify
- ✅ Create: `src/md_skill_craft/modes/mode1_guide.py`
- ✅ Modify: `src/md_skill_craft/cli.py` (integrate mode1 handler)

### Testing Requirements
- Unit tests for guide generation logic
- Mock LLM provider testing
- File I/O testing
- Template loading testing

### Success Criteria
- [x] User can describe project in 3-5 turns
- [x] LLM generates contextually appropriate md file
- [x] File saved correctly (or .suggested variant)
- [x] All unit tests pass
- [x] cli.py correctly routes to mode1_guide

## Implementation Notes
- Use existing ProviderFactory for LLM calls
- Leverage ui/menu.py for user prompts
- Reference skills/templates/ for structure guidance
- Track token usage for /cost command
