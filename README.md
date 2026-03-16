<p align="center">
  <img src="https://raw.githubusercontent.com/aayushmaanhooda/fastapi-seed/main/banner.png" alt="fastapi-seed" width="600"/>
</p>
<p align="center">
  <b>A CLI scaffold tool for FastAPI projects.</b><br/>
</p>

<p align="center">
  Stop copy-pasting project structures. One command, few questions<br/>
  and your FastAPI project is <b>scaffolded, installed, and ready to run.</b><br/><br/>
  No tutorial bloat. No manual setup. Just open your editor and start building.
</p>

<p align="center">
  <a href="https://pypi.org/project/fastapi-seed/"><img src="https://img.shields.io/pypi/v/fastapi-seed.svg" alt="PyPI version"/></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
</p>

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

---

## Changelog

### [0.1.6] - 2026-03-16

**Fixed**
- `uv` not installed now shows a clear error with install link instead of a crash (`FileNotFoundError` on Windows)
- `git` not installed now shows a clear error with install link instead of a crash
- Pressing `Ctrl+C` at any prompt now exits cleanly instead of throwing `AttributeError: 'NoneType'`

**Changed**
- Python support expanded from `>=3.13` to `>=3.11` — works on 3.11, 3.12, and 3.13

**Added**
- `--version` / `-v` flag — `fastapi-seed --version` now prints the current version and exits

### [0.1.5] - initial release
