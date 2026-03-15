"""
generator.py — renders Jinja2 templates and writes files to disk.

Key idea: instead of one giant if/else, we declare a list of
(template_path, output_path, condition) tuples. The generator
loops over them and only writes files where condition is True.

Why Jinja2?
  One template file can handle all config variants via {%if%} blocks.
  No duplicated files per variant.
"""

import subprocess
from pathlib import Path

from jinja2 import Environment, PackageLoader, StrictUndefined


def _make_env() -> Environment:
    """Create Jinja2 environment pointing at our templates/ package."""
    return Environment(
        # PackageLoader loads from src/fastapi_seed/templates/
        loader=PackageLoader("fastapi_seed", "templates"),
        # StrictUndefined raises an error if a variable is missing in a template
        # (catches typos early instead of silently rendering empty strings)
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )


def _file_map(cfg: dict) -> list[tuple[str, str]]:
    """
    Returns list of (template_name, output_relative_path) pairs.

    We use a plain list rather than filesystem glob so the mapping is
    explicit and easy to reason about — every file is visible here.
    """
    advanced = cfg["setup_type"] == "advanced"
    docker = cfg["use_docker"]
    db = cfg["database"]  # "postgresql", "sqlite", or "none"
    locust = cfg["use_locust"]
    has_db = db in ("postgresql", "sqlite")

    files = [
        # ── app core ────────────────────────────────────────
        ("app/__init__.py.jinja2", "app/__init__.py"),
        ("app/main.py.jinja2", "app/main.py"),
        ("app/routers/__init__.py.jinja2", "app/routers/__init__.py"),
        ("app/routers/health.py.jinja2", "app/routers/health.py"),
        ("app/schemas/__init__.py.jinja2", "app/schemas/__init__.py"),
        ("app/services/__init__.py.jinja2", "app/services/__init__.py"),
        ("app/core/__init__.py.jinja2", "app/core/__init__.py"),
        # ── tests ───────────────────────────────────────────
        ("tests/__init__.py.jinja2", "tests/__init__.py"),
        ("tests/test_main.py.jinja2", "tests/test_main.py"),
        # ── project root files ──────────────────────────────
        ("pyproject.toml.jinja2", "pyproject.toml"),
        ("Makefile.jinja2", "Makefile"),
        (".env.jinja2", ".env"),
        (".env.example.jinja2", ".env.example"),
        (".gitignore.jinja2", ".gitignore"),
        ("README.md.jinja2", "README.md"),
    ]

    if docker:
        files += [
            ("Dockerfile.jinja2", "Dockerfile"),
            ("docker-compose.yml.jinja2", "docker-compose.yml"),
        ]

    if docker and has_db:
        files.append(("app/core/db.py.jinja2", "app/core/db.py"))

    if advanced:
        files += [
            ("app/core/config.py.jinja2", "app/core/config.py"),
            ("app/core/logger.py.jinja2", "app/core/logger.py"),
            (".github/workflows/ci.yml.jinja2", ".github/workflows/ci.yml"),
            (".pre-commit-config.yaml.jinja2", ".pre-commit-config.yaml"),
        ]

    if locust:
        files.append(("tests/load/locustfile.py.jinja2", "tests/load/locustfile.py"))

    return files


def generate(cfg: dict, dest: Path) -> None:
    """
    Render all templates and write to dest/.
    Called by cli.py after prompts are collected.
    """
    env = _make_env()

    for tmpl_name, out_rel in _file_map(cfg):
        out_path = dest / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        template = env.get_template(tmpl_name)
        rendered = template.render(**cfg)
        out_path.write_text(rendered, encoding="utf-8")


def run_uv_sync(dest: Path) -> subprocess.CompletedProcess:
    """Run `uv sync` in the generated project directory."""
    return subprocess.run(
        ["uv", "sync"],
        cwd=dest,
        capture_output=False,
    )


def run_git_init(dest: Path) -> subprocess.CompletedProcess:
    """Run `git init` in the generated project directory."""
    return subprocess.run(
        ["git", "init"],
        cwd=dest,
        capture_output=True,
    )


def run_pre_commit_install(dest: Path) -> subprocess.CompletedProcess:
    """Run `uv run pre-commit install` to wire up git hooks (advanced only)."""
    return subprocess.run(
        ["uv", "run", "pre-commit", "install"],
        cwd=dest,
        capture_output=False,
    )
