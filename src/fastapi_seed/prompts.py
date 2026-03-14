"""
prompts.py — questionary prompt flow

Asks the user 5 questions and returns a config dict.
questionary renders arrow-key selection in the terminal (like Vite).
"""

import questionary
from questionary import Style

# Minimal style — clean dark theme
_style = Style(
    [
        ("qmark", "fg:#7c3aed bold"),       # purple question mark
        ("question", "bold"),
        ("answer", "fg:#10b981 bold"),       # green selected answer
        ("pointer", "fg:#7c3aed bold"),      # purple arrow
        ("highlighted", "fg:#7c3aed bold"),
        ("selected", "fg:#10b981"),
        ("separator", "fg:#6b7280"),
        ("instruction", "fg:#6b7280"),
    ]
)


def ask(project_name: str | None = None) -> dict:
    """Run the prompt flow and return config dict."""

    if project_name is None:
        project_name = questionary.text(
            "Project name?",
            default="my-project",
            style=_style,
        ).ask()

    setup_type = questionary.select(
        "Setup type?",
        choices=["Minimal (hobby project)", "Advanced (production project)"],
        style=_style,
    ).ask()

    use_docker = questionary.select(
        "Set up Docker?",
        choices=["Yes", "No"],
        style=_style,
    ).ask() == "Yes"

    database = "none"
    if use_docker:
        db_choice = questionary.select(
            "Which database?",
            choices=["PostgreSQL", "SQLite", "None"],
            style=_style,
        ).ask()
        database = db_choice.lower()

    use_locust = questionary.select(
        "Include load testing? (Locust)",
        choices=["Yes", "No"],
        style=_style,
    ).ask() == "Yes"

    return {
        "project_name": project_name,
        "setup_type": setup_type.split()[0].lower(),   # "minimal" or "advanced"
        "use_docker": use_docker,
        "database": database,               # "postgresql", "sqlite", or "none"
        "use_locust": use_locust,
    }
