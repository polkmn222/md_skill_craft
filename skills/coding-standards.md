---
name: Coding Standards & Best Practices
description: Python code style, type hints, naming conventions, and structure
type: reference
---

# Coding Standards Guide

Guidelines for writing clean, maintainable, and type-safe Python code.

## Core Principles

1. **Readability First** — Code is read more than written
2. **Type Safety** — Catch errors before runtime
3. **DRY (Don't Repeat Yourself)** — No duplication
4. **YAGNI (You Aren't Gonna Need It)** — Don't over-engineer
5. **Explicit Over Implicit** — Clear intent matters

## Python Style

### Naming Conventions

```python
# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Functions and variables: snake_case
def calculate_total_price(items: list[dict]) -> float:
    total = 0.0
    for item in items:
        total += item.get("price", 0)
    return total

# Classes: PascalCase
class UserRepository:
    pass

# Private functions/variables: _leading_underscore
def _format_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts).isoformat()

# Modules: snake_case
# ✓ user_service.py
# ✗ UserService.py
```

### Type Hints (Required)

Type hints are **mandatory** on all function signatures. Use Python 3.10+ union syntax.

```python
# ✓ Good: Full type hints
def fetch_user(user_id: int) -> dict[str, str] | None:
    """Fetch user by ID, return None if not found."""
    if user_id <= 0:
        raise ValueError("user_id must be positive")
    # ... implementation

# ✗ Bad: Missing return type
def fetch_user(user_id: int):
    return get_db().query(User).get(user_id)

# ✓ Complex types
from typing import Callable, TypeVar

T = TypeVar("T")
def cache_result(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator that caches function results."""
    def wrapper(*args, **kwargs) -> T:
        # ... caching logic
        return func(*args, **kwargs)
    return wrapper
```

### Docstrings (Google Style)

```python
def transfer_funds(
    from_account: str,
    to_account: str,
    amount: float,
) -> bool:
    """Transfer funds between accounts.

    Transfers the specified amount from one account to another.
    Both accounts must exist and have sufficient balance.

    Args:
        from_account: Source account ID
        to_account: Destination account ID
        amount: Amount to transfer in cents

    Returns:
        True if transfer succeeded, False otherwise

    Raises:
        ValueError: If amount is negative or accounts are the same
        AccountNotFoundError: If either account doesn't exist
        InsufficientFundsError: If source account has insufficient balance

    Example:
        >>> transfer_funds("ACC001", "ACC002", 5000)
        True
    """
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if from_account == to_account:
        raise ValueError("cannot transfer to same account")
    # ... implementation
```

## Structure & Organization

### File Layout

```python
"""Module docstring: Brief description of what this module does."""

# 1. Standard library imports
from typing import Protocol
from pathlib import Path

# 2. Third-party imports
import requests
from pydantic import BaseModel

# 3. Local imports
from app.config import settings
from app.database import db

# 4. Constants
MAX_REQUESTS_PER_SECOND = 10
DEFAULT_CACHE_TTL = 3600

# 5. Type definitions and protocols
class DataProvider(Protocol):
    def fetch(self, query: str) -> dict: ...

# 6. Exception classes
class InvalidQueryError(Exception):
    """Raised when query validation fails."""
    pass

# 7. Classes
class Service:
    """Service class implementation."""
    def __init__(self) -> None:
        self.logger = get_logger(__name__)

# 8. Functions
def process_data(data: dict) -> dict:
    """Process and validate data."""
    return data

# 9. Main entry point
if __name__ == "__main__":
    main()
```

### Import Grouping

```python
# ✓ Correct grouping
import json
from pathlib import Path
from typing import Optional

import requests
from fastapi import FastAPI

from app.models import User
from app.database import get_db

# ✗ Wrong: Mixed order
from app.database import get_db
import json
from fastapi import FastAPI
from app.models import User
```

## Anti-Patterns to Avoid

### ❌ Bare Imports
```python
# ✗ Bad: Wildcard import (pollutes namespace)
from module import *

# ✓ Good: Explicit imports
from module import specific_function, SpecificClass
```

### ❌ Bare Except
```python
# ✗ Bad: Catches all exceptions including SystemExit
try:
    something()
except:
    pass

# ✓ Good: Specific exception handling
try:
    something()
except ValueError:
    logger.warning("Invalid value")
except TimeoutError:
    logger.error("Request timed out")
```

### ❌ Magic Numbers
```python
# ✗ Bad: What does 86400 mean?
if age > 86400:
    refresh_token()

# ✓ Good: Use named constants
SECONDS_PER_DAY = 86400
if age > SECONDS_PER_DAY:
    refresh_token()
```

### ❌ Mutable Default Arguments
```python
# ✗ Bad: Default list is shared across calls!
def append_to_list(item: str, target: list[str] = []) -> list[str]:
    target.append(item)
    return target

result1 = append_to_list("a")  # ["a"]
result2 = append_to_list("b")  # ["a", "b"] — Wrong!

# ✓ Good: Use None and initialize inside
def append_to_list(item: str, target: list[str] | None = None) -> list[str]:
    if target is None:
        target = []
    target.append(item)
    return target
```

### ❌ String Formatting
```python
# ✗ Bad: String concatenation (slow, unreadable)
message = "User " + str(user_id) + " is " + str(age) + " years old"

# ✗ Old: % formatting
message = "User %s is %d years old" % (user_id, age)

# ✓ Good: f-strings (Python 3.6+)
message = f"User {user_id} is {age} years old"

# ✓ Also good: .format() for dynamic cases
template = "User {user} is {age} years old"
message = template.format(user=user_id, age=age)
```

## Advanced Patterns

### Protocol (Structural Subtyping)

```python
from typing import Protocol

class Loggable(Protocol):
    """Anything with a log method."""
    def log(self, message: str) -> None: ...

class Service:
    def log(self, message: str) -> None:
        print(f"LOG: {message}")

class Handler:
    def process(self, logger: Loggable) -> None:
        logger.log("Processing...")

# Works! No inheritance needed.
handler = Handler()
handler.process(Service())
```

### Type Guards

```python
from typing import TypeGuard

def is_user(obj: object) -> TypeGuard[User]:
    """Type guard for User instances."""
    return isinstance(obj, User) and hasattr(obj, "id")

def process(data: object) -> None:
    if is_user(data):
        # mypy knows data is User here
        print(f"User: {data.id}")
```

### Dataclasses for Immutable Data

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    """Immutable 2D point."""
    x: float
    y: float

    def distance(self) -> float:
        """Distance from origin."""
        return (self.x**2 + self.y**2) ** 0.5

# Usage
p1 = Point(3.0, 4.0)
# p1.x = 5  # Error: FrozenInstanceError (immutable)
```

## Tool Configuration

### .pylintrc or pyproject.toml (Ruff)

```toml
[tool.ruff]
target-version = "py311"
line-length = 100
exclude = [".git", ".venv", "__pycache__"]

[tool.ruff.lint]
select = ["E", "F", "I", "W", "UP", "ANN"]  # Errors, Pyflakes, isort, Warnings, Upgrade, Annotations
ignore = ["ANN101"]  # Ignore missing type for self
```

### mypy Configuration

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
```

Run mypy: `mypy app/`

## Checklist

- [ ] All functions have type hints (parameters + return)
- [ ] No wildcard imports (`from x import *`)
- [ ] No bare `except:` blocks
- [ ] No mutable default arguments
- [ ] Comments explain *why*, not *what* (code is self-documenting)
- [ ] Docstrings on all public classes/functions
- [ ] Constants in UPPER_SNAKE_CASE
- [ ] Classes and types in PascalCase
- [ ] Functions and variables in snake_case
- [ ] No magic numbers (use named constants)
- [ ] Proper error handling (specific exceptions, not bare except)
- [ ] Tests written alongside code

## References

- [PEP 8 — Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [PEP 484 — Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
