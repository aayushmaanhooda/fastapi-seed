"""
prompts.py — questionary prompt flow

Asks the user 5 questions and returns a config dict.
questionary renders arrow-key selection in the terminal.
After each answer, _checkpoint() overwrites the questionary line with a
green ✓ summary — giving a Vite-style checkpoint feel.
"""

import sys

import questionary
from questionary import Style
from rich import print as rprint

# ◇ hollow while active → replaced by ✓ green after answered
_style = Style(
    [
        ("qmark", "fg:#7c3aed bold"),  # ◇ purple hollow diamond
        ("question", "fg:#a78bfa bold"),  # purple question text
        ("answer", "fg:#10b981 bold"),  # green answer (fallback if no tty)
        ("pointer", "fg:#7c3aed bold"),  # purple arrow
        ("highlighted", "fg:#7c3aed bold"),
        ("selected", "fg:#10b981"),
        ("separator", "fg:#6b7280"),
        ("instruction", "fg:#6b7280"),
    ]
)


def _checkpoint(label: str, value: str) -> None:
    """
    Overwrite the questionary answered line with a green ✓ checkpoint.

    After .ask() returns, the cursor sits one line below the answered prompt.
    ESC[1A moves up to that line, ESC[2K erases it, then we reprint it as
    a clean green ✓ summary — turning every answered question into a receipt.
    """
    if sys.stdout.isatty():
        sys.stdout.write("\033[1A\033[2K\r")
        sys.stdout.flush()
    rprint(f"[bold #10b981]✓[/] [#6b7280]{label}[/]  [bold white]{value}[/]")


def ask(project_name: str | None = None) -> dict:
    """Run the prompt flow and return config dict."""

    if project_name is None:
        project_name = questionary.text(
            "Project name?",
            default="my-project",
            qmark="◇",
            style=_style,
        ).ask()
        if project_name is None:
            raise KeyboardInterrupt
        _checkpoint("Project name", project_name)

    setup_type = questionary.select(
        "Setup type?",
        choices=["Minimal (hobby project)", "Advanced (production project)"],
        qmark="◇",
        style=_style,
    ).ask()
    if setup_type is None:
        raise KeyboardInterrupt
    _checkpoint("Setup type", setup_type)

    docker_ans = questionary.select(
        "Set up Docker?",
        choices=["Yes", "No"],
        qmark="◇",
        style=_style,
    ).ask()
    if docker_ans is None:
        raise KeyboardInterrupt
    _checkpoint("Docker", docker_ans)
    use_docker = docker_ans == "Yes"

    database = "none"
    if use_docker:
        db_choice = questionary.select(
            "Which database?",
            choices=["PostgreSQL", "SQLite", "None"],
            qmark="◇",
            style=_style,
        ).ask()
        if db_choice is None:
            raise KeyboardInterrupt
        _checkpoint("Database", db_choice)
        database = db_choice.lower()

    locust_ans = questionary.select(
        "Include load testing? (Locust)",
        choices=["Yes", "No"],
        qmark="◇",
        style=_style,
    ).ask()
    if locust_ans is None:
        raise KeyboardInterrupt
    _checkpoint("Load testing", locust_ans)
    use_locust = locust_ans == "Yes"

    return {
        "project_name": project_name,
        "setup_type": setup_type.split()[0].lower(),  # "minimal" or "advanced"
        "use_docker": use_docker,
        "database": database,  # "postgresql", "sqlite", or "none"
        "use_locust": use_locust,
    }
