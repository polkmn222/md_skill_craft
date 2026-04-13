---
name: Code Validation & Testing
description: Lint, type checking, unit tests, and validation strategies
type: reference
---

# Code Validation Guide

Testing and validation layered approach: lint → typecheck → unit tests → integration tests.

## The Validation Pyramid

```
        ┌─────────────────┐
        │  Manual/Smoke   │  Run once before shipping
        │  (5% of effort) │
        ├─────────────────┤
        │ Integration     │  End-to-end tests (mocked APIs)
        │ (15% of effort) │
        ├─────────────────┤
        │ Unit Tests      │  Fast, focused, high coverage
        │ (50% of effort) │
        ├─────────────────┤
        │ Type Checking   │  mypy, pyright (automated)
        │ (20% of effort) │
        ├─────────────────┤
        │ Linting         │  ruff, pylint (automated)
        │ (10% of effort) │
        └─────────────────┘
```

## Layer 1: Linting (Automated Code Quality)

### Setup

```toml
# pyproject.toml
[tool.ruff]
target-version = "py311"
line-length = 100
exclude = [".git", ".venv", "build"]

[tool.ruff.lint]
select = ["E", "F", "I", "W", "UP", "ANN"]
ignore = ["ANN101"]  # self parameter
```

### Commands

```bash
# Check for violations
ruff check app/

# Auto-fix fixable violations
ruff check --fix app/

# Format code
ruff format app/

# Check single file
ruff check app/main.py
```

### What it checks
- **E**: Errors (spacing, indentation)
- **F**: Pyflakes (undefined names, unused imports)
- **I**: isort (import ordering)
- **W**: Warnings (deprecated constructs)
- **UP**: Upgrade (modernize Python syntax)
- **ANN**: Annotations (type hints present)

## Layer 2: Type Checking (Catch Type Errors)

### Setup

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "third_party.*"
ignore_missing_imports = true
```

### Commands

```bash
# Type-check all files
mypy app/

# Type-check single file
mypy app/main.py

# Suppress specific error on one line
x = some_untyped_func()  # type: ignore[no-untyped-call]
```

### Common Issues & Fixes

```python
# ❌ Error: Missing parameter type
def greet(name):  # Error: Parameter "name" is missing a type annotation

# ✓ Fix: Add type
def greet(name: str) -> None:
    print(f"Hello, {name}")

# ❌ Error: Missing return type
def process(data: dict) -> None:  # Should not return dict
    return {"result": "done"}

# ✓ Fix: Add return type
def process(data: dict) -> dict:
    return {"result": "done"}

# ❌ Error: Incompatible type
x: int = "not an int"

# ✓ Fix: Use Union for multiple types
from typing import Union
x: Union[int, str] = "ok"
# or (Python 3.10+)
x: int | str = "ok"
```

## Layer 3: Unit Tests (Fast, Focused Tests)

### Pytest Setup

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = "-v --strict-markers"
```

### Test File Structure

```python
# tests/test_user_service.py
import pytest
from unittest.mock import Mock
from app.user_service import UserService

@pytest.fixture
def user_service() -> UserService:
    """Fixture: UserService with mocked database."""
    db = Mock()
    return UserService(db)

class TestUserService:
    """Test suite for UserService."""

    def test_create_user_success(self, user_service: UserService) -> None:
        """Test successful user creation."""
        result = user_service.create("alice", "alice@example.com")
        assert result.id is not None
        assert result.email == "alice@example.com"

    def test_create_user_invalid_email(self, user_service: UserService) -> None:
        """Test that invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email"):
            user_service.create("alice", "not-an-email")

    @pytest.mark.parametrize("email", ["bad", "no-domain", ""])
    def test_invalid_emails(self, user_service: UserService, email: str) -> None:
        """Test multiple invalid email formats."""
        with pytest.raises(ValueError):
            user_service.create("alice", email)
```

### Run Tests

```bash
# Run all tests
pytest tests/

# Run specific file
pytest tests/test_user_service.py

# Run specific test
pytest tests/test_user_service.py::TestUserService::test_create_user_success

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run marked tests
pytest -m "not slow"  # Skip slow tests
```

### Mocking External Dependencies

```python
import pytest
from unittest.mock import Mock, patch, MagicMock

class TestAPIClient:
    @patch("requests.get")
    def test_fetch_user_success(self, mock_get: Mock) -> None:
        """Test API client with mocked HTTP response."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1, "name": "Alice"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client = APIClient()
        user = client.fetch_user(1)

        assert user["name"] == "Alice"
        mock_get.assert_called_once_with("https://api.example.com/users/1")
```

## Layer 4: Integration Tests

Integration tests use real (or realistic) dependencies but avoid slow external services.

```python
# tests/test_integration.py
import pytest
from app.main import app
from app.database import DB

@pytest.fixture
def db() -> DB:
    """Fixture: Real database in test mode."""
    db = DB(":memory:")  # SQLite in-memory for tests
    yield db
    db.cleanup()

class TestUserIntegration:
    def test_create_and_fetch_user(self, db: DB) -> None:
        """Integration: Create user, then fetch it."""
        service = UserService(db)
        
        # Create
        created = service.create("alice", "alice@example.com")
        
        # Fetch
        fetched = service.get(created.id)
        
        assert fetched.email == "alice@example.com"
```

## Layer 5: Manual Smoke Tests

Run before shipping. Focus on happy paths and obvious edge cases.

- [ ] Can I start the app without errors?
- [ ] Does the Web UI load?
- [ ] Can I perform a simple action (translate, generate doc)?
- [ ] Does it handle missing API keys gracefully?
- [ ] Are error messages helpful?
- [ ] Does it work across all supported providers (Claude, GPT, Gemini)?

## Full Validation Checklist

```bash
# 1. Lint
ruff check app/ tests/
ruff format --check app/ tests/

# 2. Type check
mypy app/

# 3. Run tests
pytest tests/ -v

# 4. Coverage report
pytest tests/ --cov=app --cov-report=term-missing

# 5. Security scan (optional)
bandit -r app/
```

### All-in-One Script

```bash
#!/bin/bash
set -e  # Exit on first error

echo "🔍 Linting..."
ruff check app/ tests/

echo "🔍 Type checking..."
mypy app/

echo "🧪 Running tests..."
pytest tests/ -v

echo "✅ All validations passed!"
```

Save as `scripts/validate.sh`, then run `make check` or `bash scripts/validate.sh`.

## Test Coverage Goals

| Code Type | Coverage Target |
|-----------|-----------------|
| Business logic (core/) | 80%+ |
| Features (features/) | 70%+ |
| Config/Utils | 50%+ |
| Integration/CLI | 30%+ (hard to test fully) |

Check coverage:
```bash
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html
```

## Continuous Integration (Optional)

If using GitHub Actions:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: ruff check app/ tests/
      - run: mypy app/
      - run: pytest tests/ --cov=app
```

## Key Principles

1. **Test Behavior, Not Implementation** — Assert what users care about, not internal details
2. **Mocks at System Boundaries** — Mock APIs, databases, filesystems; don't mock logic
3. **Name Tests Clearly** — `test_create_user_with_invalid_email_raises_error` (long is fine)
4. **One Assertion Per Test** — Or test one concept per test
5. **DRY With Fixtures** — Use `conftest.py` for shared setup
6. **Fast Tests First** — Unit tests < 1s, integration < 10s

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Ruff](https://docs.astral.sh/ruff/)
- [mypy](https://mypy.readthedocs.io/)
