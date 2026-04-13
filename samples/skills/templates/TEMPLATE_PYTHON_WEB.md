# [PROJECT_NAME]

## Project
[One-line project description]
**Stack**: FastAPI/Django/Flask, PostgreSQL/MongoDB, Python 3.x

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Key Commands
| Task | Command |
|------|---------|
| Dev Server | `fastapi dev src/main.py` (or `python manage.py runserver`) |
| Tests | `pytest tests/ -v` |
| Type Check | `mypy src/` |
| Lint | `ruff check src/` |
| Format | `ruff format src/` |
| Migrations | `alembic upgrade head` (or `python manage.py migrate`) |
| Database | `psql -d dbname` (or your DB CLI) |

## Architecture
- `src/` — Main application code
  - `api/` — API routes/endpoints
  - `models/` — Database models (SQLAlchemy/ORM)
  - `schemas/` — Pydantic request/response schemas
  - `services/` — Business logic (decoupled from routes)
  - `db/` — Database connections and session management
  - `config.py` — Settings and environment variables
- `tests/` — Unit and integration tests
- `migrations/` — Database migrations (Alembic)
- `.env` — Environment variables (DO NOT commit!)
- `requirements.txt` — Python dependencies

## Conventions
- Type hints required on all functions (mypy strict)
- Docstrings: Google style
- Services layer for business logic (not in routes)
- Dependency injection for testability
- Never commit `.env` file
- Database models separate from API schemas
- All API responses use consistent structure

## Key Dependencies
- **FastAPI** / Django / Flask — Web framework
- **Pydantic** — Data validation
- **SQLAlchemy** — ORM
- **Alembic** — Database migrations
- **pytest** — Testing
- **httpx** — Async HTTP client for tests

## Anti-Patterns
- ❌ Database logic in route handlers
- ❌ Missing type hints
- ❌ Committing `.env` with secrets
- ❌ No tests for services
- ❌ Hardcoded values (use config)

## Skills
@skills/coding-standards.md @skills/validation.md @skills/orchestration.md

## Database
- **Connection**: See `.env` for DATABASE_URL
- **Migrations**: `alembic upgrade head` before running
- **Seeding**: See `scripts/seed_db.py`

## Deployment
```bash
make build   # Build Docker image
make deploy  # Deploy to [platform]
```

## Development Workflow
1. Create feature branch
2. Write tests first (TDD)
3. Implement feature in `src/`
4. Run `make check` (lint, type, test)
5. Push and create PR
6. CI/CD pipeline validates
7. Merge after approval
