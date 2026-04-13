# [PROJECT_NAME]

## Project
[One-line CLI tool description]
**Stack**: Click / Typer, Python 3.11+, pytest

## Setup
```bash
pip install -e .
# or: python -m pip install -e .
```

## Key Commands
| Task | Command |
|------|---------|
| CLI | `[tool-name] --help` |
| Dev | `python -m [package].cli --help` |
| Tests | `pytest tests/ -v` |
| Type Check | `mypy src/` |
| Lint | `ruff check src/ tests/` |
| Format | `ruff format src/ tests/` |

## Architecture
- `src/[package]/` — Source code
  - `cli.py` — Click/Typer commands entry point
  - `commands/` — Command implementations
    - `__init__.py`
    - `[command_name].py`
  - `core/` — Core logic
    - `__init__.py`
    - `processor.py` (main logic)
    - `errors.py`
  - `utils/` — Utilities
    - `__init__.py`
    - `formatting.py`
    - `validation.py`
  - `__init__.py`
- `tests/` — Unit tests (pytest)
  - `test_cli.py`
  - `test_commands/`
  - `test_core/`
- `pyproject.toml` — Project metadata
- `README.md` — Usage guide

## Conventions
- TypeScript strict mode required (use mypy strict mode)
- Click groups for command organization
- Each command in separate file for testability
- Type hints on all functions
- Google-style docstrings
- Commands should be pure functions when possible (testable)
- Click callbacks for validation

## Key Dependencies
- **Click** / **Typer** — CLI framework
- **Python 3.11+** — Type hints, match statements
- **pytest** — Testing
- **mypy** — Type checking
- **ruff** — Linting/formatting

## CLI Structure (Click)

```python
# src/myapp/cli.py
import click
from myapp.commands import process_command

@click.group()
@click.version_option()
def cli():
    """My CLI tool."""
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def process(input_file: str, output: str | None, verbose: bool) -> None:
    """Process input file."""
    result = process_command(input_file, verbose)
    if output:
        click.echo(f"Wrote to {output}")
    else:
        click.echo(result)

if __name__ == '__main__':
    cli()
```

## CLI Structure (Typer)

```python
# src/myapp/cli.py
import typer
from myapp.commands import process_command

app = typer.Typer(help="My CLI tool.")

@app.command()
def process(
    input_file: str = typer.Argument(..., help="Input file path"),
    output: str | None = typer.Option(None, '--output', '-o', help="Output file"),
    verbose: bool = typer.Option(False, '--verbose', '-v', help="Verbose output")
) -> None:
    """Process input file."""
    result = process_command(input_file, verbose)
    if output:
        typer.echo(f"Wrote to {output}")
    else:
        typer.echo(result)

if __name__ == '__main__':
    app()
```

## Testing CLI
```python
from click.testing import CliRunner
from myapp.cli import cli

def test_process_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['process', 'input.txt'])
    assert result.exit_code == 0
    assert 'Wrote to' in result.output

def test_process_with_output():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('input.txt', 'w') as f:
            f.write('test')
        result = runner.invoke(cli, ['process', 'input.txt', '-o', 'output.txt'])
        assert result.exit_code == 0
```

## Anti-Patterns
- ❌ Logic directly in CLI callback (hard to test)
- ❌ Global state or file handles (use dependency injection)
- ❌ Untyped arguments/options
- ❌ No error messages (use click.ClickException)
- ❌ Direct print() (use click.echo)

## Error Handling
```python
# Use Click exceptions for user-facing errors
try:
    result = process_file(path)
except FileNotFoundError as e:
    raise click.FileError(str(path), str(e))
except ValueError as e:
    raise click.BadParameter(str(e))
```

## Distribution
```bash
# Build
pip install build
python -m build

# Upload to PyPI
pip install twine
twine upload dist/*
```

## Development Workflow
1. Create command in `commands/`
2. Implement logic in `core/`
3. Write tests for logic in `tests/`
4. Run `pytest tests/` to verify
5. Test CLI manually: `python -m [package].cli [command]`
6. Run `make check` (lint → typecheck → test)
7. Commit and push

## Skills
@skills/coding-standards.md @skills/validation.md @skills/orchestration.md

## References
- [Click Documentation](https://click.palletsprojects.com/)
- [Typer Documentation](https://typer.tiangolo.com/)
