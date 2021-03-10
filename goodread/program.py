import typer
from typing import Optional
from .document import Document
from . import config


# Program

program = typer.Typer()


# Helpers


def version(value: bool):
    if value:
        typer.echo(config.VERSION)
        raise typer.Exit()


# Command


@program.command()
def program_main(
    path: str = typer.Argument(..., help="Path to markdown"),
    write: bool = typer.Option(default=False, help="Write the results inline"),
    version: Optional[bool] = typer.Option(None, "--version", callback=version),
):
    """Goodread executes Python and Bash codeblocks in Markdown and writes the results back."""
    document = Document(path)
    text = document.process(write=write)
    if not write:
        typer.secho(text)
