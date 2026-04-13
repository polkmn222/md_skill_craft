---
name: Claude Code Hooks Configuration
description: Setting up pre/post hooks in settings.json to automate validation and protection
type: reference
---

# Claude Code Hooks Guide

Automate validation and protection using hooks triggered by Claude Code tool use.

## What Are Hooks?

Hooks are shell scripts that run **automatically** when Claude Code uses tools. They let you:
- Validate before action (pre-hooks): "Is this bash command safe?"
- Clean up after action (post-hooks): "Format this code"
- Protect sensitive files: "Don't commit .env!"
- Enforce standards: "Run linter on all edits"

**Key**: Hooks run **in the harness**, not in Claude's mind. You must return exit codes.

## Hook Return Codes

```bash
exit 0  # ✓ Allow (proceed with tool use)
exit 1  # ✗ Block (prevent tool use, Claude sees error)
exit 2  # ⚠️  Warn (proceed but show warning to Claude)
```

## Hook Types

### Pre-Tool Hooks (Before Action)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "bash scripts/check-bash.sh"}
        ]
      }
    ]
  }
}
```

Runs **before** Bash tool executes. See what Claude is about to run, decide whether to allow it.

### Post-Tool Hooks (After Action)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {"type": "command", "command": "ruff check ${CLAUDE_TOOL_OUTPUT_PATH}"}
        ]
      }
    ]
  }
}
```

Runs **after** tool finishes. Validate or transform the result.

## Hook Matchers

Which tool triggers the hook?

| Matcher | Triggered By |
|---------|--------------|
| `Bash` | `Bash` tool (terminal commands) |
| `Edit` | `Edit` tool (file modifications) |
| `Write` | `Write` tool (new files) |
| `Read` | `Read` tool (file reads) |
| `Agent` | Spawning a new agent |

## Environment Variables

Hooks receive context via environment variables:

### Pre-Hook Env Vars

```bash
# What Claude is about to do
$CLAUDE_TOOL_NAME        # "Bash", "Edit", "Write", "Agent"
$CLAUDE_TOOL_INPUT       # The command/file path/content
$CLAUDE_TOOL_INPUT_PATH  # If applicable (file path)
```

### Post-Hook Env Vars

```bash
# What Claude just did
$CLAUDE_TOOL_NAME         # "Bash", "Edit", etc.
$CLAUDE_TOOL_OUTPUT_PATH  # Path to created/modified file
$CLAUDE_TOOL_EXIT_CODE    # Exit code of the tool
```

## Examples

### Example 1: Protect .env Files

Block reading or editing .env files (except explicit allow).

```bash
# scripts/protect-env.sh
#!/bin/bash

if [[ "$CLAUDE_TOOL_INPUT_PATH" == *".env"* ]]; then
    echo "❌ Error: Cannot edit .env files (contains secrets)"
    exit 1
fi

exit 0  # Allow
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {"type": "command", "command": "bash scripts/protect-env.sh"}
        ]
      }
    ]
  }
}
```

### Example 2: Auto-Format on Edit

Run `ruff format` after every file edit.

```bash
# scripts/auto-format.sh
#!/bin/bash

FILE="$CLAUDE_TOOL_OUTPUT_PATH"

if [[ "$FILE" == *.py ]]; then
    echo "🔧 Formatting $FILE..."
    ruff format "$FILE"
    if [[ $? -eq 0 ]]; then
        echo "✓ Formatted"
        exit 0
    else
        echo "❌ Formatting failed"
        exit 1
    fi
fi

exit 0  # Non-Python files, allow
```

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {"type": "command", "command": "bash scripts/auto-format.sh"}
        ]
      }
    ]
  }
}
```

### Example 3: Prevent Destructive Bash

Block dangerous bash commands.

```bash
# scripts/check-bash-safety.sh
#!/bin/bash

COMMAND="$CLAUDE_TOOL_INPUT"

# Dangerous patterns
DANGEROUS=(
    "rm -rf /"
    "rm -rf ~"
    "dd if=/dev/zero"
    ": () { : | :& };"  # fork bomb
    "mkfs"               # format filesystem
    "dd of=/dev/"
)

for pattern in "${DANGEROUS[@]}"; do
    if [[ "$COMMAND" == *"$pattern"* ]]; then
        echo "❌ Error: Refusing dangerous command: $COMMAND"
        exit 1
    fi
done

# Warn about sudo
if [[ "$COMMAND" == sudo* ]]; then
    echo "⚠️ Warning: Using sudo. Ensure this is necessary."
fi

exit 0  # Allow
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "bash scripts/check-bash-safety.sh"}
        ]
      }
    ]
  }
}
```

### Example 4: Type-Check on Python Edit

Run mypy after editing Python files.

```bash
# scripts/typecheck-on-edit.sh
#!/bin/bash

FILE="$CLAUDE_TOOL_OUTPUT_PATH"

if [[ "$FILE" == *.py ]]; then
    echo "🔍 Type-checking $FILE..."
    mypy "$FILE" --no-error-summary 2>/dev/null
    if [[ $? -eq 0 ]]; then
        echo "✓ Type check passed"
        exit 0
    else
        echo "⚠️ Type check failed (but allowing edit)"
        exit 0  # Allow even if type check fails
    fi
fi

exit 0
```

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {"type": "command", "command": "bash scripts/typecheck-on-edit.sh"}
        ]
      }
    ]
  }
}
```

### Example 5: Validate Commit Message

Enforce commit message format.

```bash
# scripts/validate-commit.sh
#!/bin/bash

# Extract commit message from Bash command
# This is a simplified example
MESSAGE="$CLAUDE_TOOL_INPUT"

# Check format: [CATEGORY] Description
if ! [[ "$MESSAGE" =~ ^\[.*\]\ .* ]]; then
    echo "❌ Error: Commit message must match: [CATEGORY] Description"
    echo "  Example: [FEAT] Add user authentication"
    exit 1
fi

# Check minimum length
if [[ ${#MESSAGE} -lt 10 ]]; then
    echo "❌ Error: Commit message too short (minimum 10 chars)"
    exit 1
fi

exit 0
```

## Common Hook Patterns

### Pattern: Validate Python Syntax

```bash
#!/bin/bash
python -m py_compile "$CLAUDE_TOOL_OUTPUT_PATH"
```

### Pattern: Check File Size

```bash
#!/bin/bash
SIZE=$(stat -c%s "$CLAUDE_TOOL_OUTPUT_PATH")
if [[ $SIZE -gt 10000 ]]; then  # 10KB limit
    echo "❌ File too large"
    exit 1
fi
exit 0
```

### Pattern: Verify Test Coverage

```bash
#!/bin/bash
if [[ "$CLAUDE_TOOL_OUTPUT_PATH" == */test_*.py ]]; then
    pytest --cov=app "$CLAUDE_TOOL_OUTPUT_PATH" --cov-fail-under=80
fi
```

### Pattern: Prevent Secrets Leak

```bash
#!/bin/bash
if grep -qE "(password|api_key|secret|token)" "$CLAUDE_TOOL_OUTPUT_PATH"; then
    echo "❌ Error: File contains secrets"
    exit 1
fi
exit 0
```

## Configuration Template

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash scripts/validate-bash.sh"
          }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash scripts/protect-secrets.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "ruff check ${CLAUDE_TOOL_OUTPUT_PATH}"
          },
          {
            "type": "command",
            "command": "mypy ${CLAUDE_TOOL_OUTPUT_PATH}"
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash scripts/validate-new-file.sh"
          }
        ]
      }
    ]
  }
}
```

## Best Practices

### ✓ Do

- **Keep hooks fast**: <1 second per hook
- **Clear error messages**: Tell Claude why it failed
- **Log to stderr**: `echo "Error" >&2`
- **Exit 0 by default**: Don't block unless necessary
- **Test hooks locally**: Run `bash scripts/hook.sh` manually first
- **Use specific matchers**: Don't over-block

### ✗ Don't

- **Block everything**: Hooks should enable, not prevent
- **Slow validation**: If mypy takes 10s, run it post-tool instead
- **Cryptic error messages**: Claude won't understand why it failed
- **Assume variables exist**: Always check `[ -z "$VAR" ]` first
- **Make hooks too strict**: Sometimes imperfect code is OK

## Debugging Hooks

If hooks aren't working:

1. **Test manually**:
   ```bash
   export CLAUDE_TOOL_INPUT_PATH="path/to/file.py"
   bash scripts/my-hook.sh
   echo $?  # Print exit code
   ```

2. **Add debug output**:
   ```bash
   #!/bin/bash
   echo "DEBUG: File is $CLAUDE_TOOL_OUTPUT_PATH" >&2
   mypy "$CLAUDE_TOOL_OUTPUT_PATH"
   ```

3. **Check settings.json syntax**:
   ```bash
   python -m json.tool ~/.claude/settings.json
   ```

4. **Verify the matcher name**:
   - Use exact tool names: `Bash`, `Edit`, `Write`, not `bash`, `edit`

## Hooks vs. Git Hooks

| Aspect | Claude Hooks | Git Hooks |
|--------|--------------|-----------|
| Triggered by | Claude Code tools | git commands |
| Run | In harness | In repo |
| Access to | Tool input/output | Staged files |
| When | Before/after tool use | Before/after git command |
| Use Case | Validate edits | Validate commits |

You can use **both**. Git hooks validate commits; Claude hooks validate work before commit.

## Summary

Hooks automate validation and protection without slowing down development. Start simple (protect .env), expand as needed (auto-format, typecheck).

**The Goal**: Make it impossible to make obvious mistakes.
