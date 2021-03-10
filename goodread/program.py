import typer
from typing import Optional
from . import config


# Program

program = typer.Typer()


# Helpers


def version(value: bool):
    if value:
        typer.echo(config.VERSION)
        raise typer.Exit()


# Command


@program.callback()
def program_main(
    version: Optional[bool] = typer.Option(None, "--version", callback=version)
):
    """Goodread executes Python and Bash codeblocks in Markdown and writes the results back."""
    pass
