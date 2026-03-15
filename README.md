<p align="center">
  <img src="banner.png" alt="fastapi-seed" width="600"/>
</p>

### 🌱 Scaffold a production-ready or hobby-ready FastAPI project setup in seconds.

[![PyPI version](https://img.shields.io/pypi/v/fastapi-seed.svg)](https://pypi.org/project/fastapi-seed/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- **Scaffold a production-ready or hobby-ready FastAPI project in seconds.** -->

Like `create-vite` but for Python, answer 5 questions, get a fully structured FastAPI project ready to run.

```bash
uvx fastapi-seed init my-project   # scaffold into new folder
uvx fastapi-seed init .            # scaffold into current folder
```

---

## Install

```bash
# recommended — no install needed
uvx fastapi-seed init my-project

# or install globally
pip install fastapi-seed
uv add fastapi-seed
```

## What you get

Answer 5 questions:

```
1. Project name?
2. Setup type?          Minimal / Advanced
3. Set up Docker?       Yes / No
4. Which database?      PostgreSQL / SQLite / None   (only if Docker = Yes)
5. Load testing?        Yes / No
```

A fully structured project is generated and dependencies are installed automatically via `uv sync`.

### Always included

```
my-project/
├── app/
│   ├── main.py              ← clean, minimal (~15 lines)
│   ├── routers/health.py    ← health check endpoint
│   ├── schemas/
│   ├── services/
│   └── core/
├── tests/test_main.py
├── .env + .env.example
├── Makefile
├── pyproject.toml           ← ruff + pytest configured
└── README.md
```

### Advanced setup adds

```
app/core/config.py           ← pydantic-settings config
app/core/logger.py           ← structured logging
.github/workflows/ci.yml     ← ruff + pytest on every PR
.pre-commit-config.yaml      ← ruff runs before every commit
```

### Docker + database adds

```
Dockerfile                   ← single stage (minimal) / multi-stage (advanced)
docker-compose.yml           ← app + db service pre-wired
app/core/db.py               ← SQLModel session + engine
```

### Load testing adds

```
tests/load/locustfile.py     ← Locust hitting health endpoint
```

## Why fastapi-seed?

| | fastapi-seed | others |
|---|---|---|
| Package manager | `uv` | pip |
| main.py | 15 lines, clean | 100+ lines of tutorial code |
| Load testing | ✓ Locust included | ✗ |
| Complexity levels | Minimal / Advanced | one size fits all |
| Docker + DB | pre-wired, just works | manual setup |
| CI/CD | GitHub Actions included | ✗ |
| Interactive UX | arrow-key prompts (like Vite) | basic input() |

## Generated project commands

```bash
make dev          # uv run uvicorn app.main:app --reload
make test         # uv run pytest
make lint         # uv run ruff check .
make format       # uv run ruff format .
make docker-up    # docker compose up --build
make load-test    # uv run locust
```

## License

MIT
