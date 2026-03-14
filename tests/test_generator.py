"""
Basic smoke tests for the generator.

We generate into a temp directory and assert the expected files exist.
We do NOT test file content in depth — that would just be re-testing Jinja2.
"""

from pathlib import Path

from fastapi_seed.generator import generate


MINIMAL_CFG = {
    "project_name": "test-project",
    "setup_type": "minimal",
    "use_docker": False,
    "database": "none",
    "use_locust": False,
}

ADVANCED_CFG = {
    "project_name": "test-project",
    "setup_type": "advanced",
    "use_docker": True,
    "database": "postgresql",
    "use_locust": True,
}


def test_minimal_generates_core_files(tmp_path: Path):
    generate(MINIMAL_CFG, tmp_path)
    assert (tmp_path / "app" / "main.py").exists()
    assert (tmp_path / "app" / "routers" / "health.py").exists()
    assert (tmp_path / "tests" / "test_main.py").exists()
    assert (tmp_path / "pyproject.toml").exists()
    assert (tmp_path / "Makefile").exists()
    assert (tmp_path / ".env").exists()
    assert (tmp_path / ".gitignore").exists()


def test_minimal_no_docker_files(tmp_path: Path):
    generate(MINIMAL_CFG, tmp_path)
    assert not (tmp_path / "Dockerfile").exists()
    assert not (tmp_path / "docker-compose.yml").exists()


def test_minimal_no_advanced_files(tmp_path: Path):
    generate(MINIMAL_CFG, tmp_path)
    assert not (tmp_path / "app" / "core" / "config.py").exists()
    assert not (tmp_path / "app" / "core" / "logger.py").exists()
    assert not (tmp_path / ".github").exists()


def test_advanced_generates_extra_files(tmp_path: Path):
    generate(ADVANCED_CFG, tmp_path)
    assert (tmp_path / "Dockerfile").exists()
    assert (tmp_path / "docker-compose.yml").exists()
    assert (tmp_path / "app" / "core" / "config.py").exists()
    assert (tmp_path / "app" / "core" / "logger.py").exists()
    assert (tmp_path / "app" / "core" / "db.py").exists()
    assert (tmp_path / ".github" / "workflows" / "ci.yml").exists()
    assert (tmp_path / ".pre-commit-config.yaml").exists()
    assert (tmp_path / "tests" / "load" / "locustfile.py").exists()


def test_main_py_is_minimal(tmp_path: Path):
    generate(MINIMAL_CFG, tmp_path)
    content = (tmp_path / "app" / "main.py").read_text()
    lines = [line for line in content.splitlines() if line.strip()]
    assert len(lines) <= 20, f"main.py has {len(lines)} non-empty lines — keep it under 20"


def test_project_name_in_main(tmp_path: Path):
    generate(MINIMAL_CFG, tmp_path)
    content = (tmp_path / "app" / "main.py").read_text()
    assert "test-project" in content


def test_docker_compose_has_db_service(tmp_path: Path):
    generate(ADVANCED_CFG, tmp_path)
    content = (tmp_path / "docker-compose.yml").read_text()
    assert "postgres" in content
