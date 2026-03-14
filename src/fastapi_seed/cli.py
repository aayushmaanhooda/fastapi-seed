"""
cli.py — typer entry point for fastapi-seed.

Why typer?
  Built by the same author as FastAPI. Uses Python type hints for
  argument parsing — no argparse boilerplate, automatic --help.

Why rich?
  Gives us colored output and a spinner during uv sync for free.
  We keep it minimal: just enough to feel polished without being loud.
"""

from pathlib import Path

import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from fastapi_seed import prompts
from fastapi_seed.generator import generate, run_uv_sync

app = typer.Typer(
    help="Scaffold a FastAPI project in seconds.",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()


@app.callback()
def _main() -> None:
    """fastapi-seed — scaffold FastAPI projects in seconds."""


def _banner() -> None:
    """Print a minimal welcome banner."""
    text = Text()
    text.append("🌱  ")
    text.append("fastapi", style="bold #7c3aed")
    text.append("-seed", style="bold #10b981")
    text.append("  ·  scaffold FastAPI projects in seconds", style="dim")
    rprint(Panel(text, border_style="dim", padding=(0, 2)))
    print()


def _success_panel(project_name: str, dest: Path, cfg: dict) -> None:
    """Print the post-scaffold instructions."""
    lines = [f"[bold green]✓[/] Project [bold]{project_name}[/] created",
             "[bold green]✓[/] Dependencies installed via uv", ""]

    if dest.name != ".":
        lines.append(f"  [dim]cd[/] [bold]{dest.name}[/]")

    lines += [
        "",
        "  [dim]Run locally:[/]",
        "    [bold cyan]uv run uvicorn app.main:app --reload[/]",
    ]

    if cfg["use_docker"]:
        lines += [
            "",
            "  [dim]Run with Docker:[/]",
            "    [bold cyan]docker compose up[/]",
        ]

    console.print(Panel("\n".join(lines), border_style="green", padding=(1, 2)))


@app.command()
def init(
    project_name: str = typer.Argument(
        ...,
        help='Project folder name, or "." for current directory.',
    ),
) -> None:
    """Scaffold a new FastAPI project."""
    _banner()

    # Resolve destination path
    if project_name == ".":
        dest = Path.cwd()
        name_for_prompts = dest.name
    else:
        dest = Path.cwd() / project_name
        name_for_prompts = project_name

    # Collect answers — pass name so we skip re-asking if given as arg
    try:
        cfg = prompts.ask(project_name=name_for_prompts)
    except KeyboardInterrupt:
        rprint("\n[dim]Cancelled.[/]")
        raise typer.Exit(1)

    print()

    # Generate files
    with console.status("[bold #7c3aed]Generating files...[/]", spinner="dots"):
        dest.mkdir(parents=True, exist_ok=True)
        generate(cfg, dest)

    rprint("[bold green]✓[/] Files generated")

    # Run uv sync
    with console.status("[bold #7c3aed]Installing dependencies (uv sync)...[/]", spinner="dots"):
        result = run_uv_sync(dest)

    if result.returncode != 0:
        rprint("[bold red]✗[/] uv sync failed — run it manually inside the project folder.")
    else:
        rprint("[bold green]✓[/] Dependencies installed")

    print()
    _success_panel(cfg["project_name"], dest, cfg)
