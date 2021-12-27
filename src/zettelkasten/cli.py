# zettelkasten/cli.py
# type: ignore[attr-defined]
"""Module aggregating the command line interface."""
import configparser
import logging
import os
import platform
import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import IntPrompt
from rich.prompt import Prompt
from rich.theme import Theme

from . import __version__
from . import add as zadd
from . import compile as comp
from . import defaults
from . import monkeypatch
from . import parse

logger = logging.getLogger(__name__)

# monkey patch
zk_path = Path.home() / ".zettelkasten.d" / "zk.cfg"
monkeypatch.patch_defaults(zk_path)

custom_theme = Theme(
    {
        "info": "dim cyan",
        "warning": "magenta",
        "danger": "bold red",
        "def": "bold cyan",
        "req": "bold green",
    }
)

app = typer.Typer(
    name="zettelkasten",
    help="Folder based zettelkasten with a bibtex reference system and emacs "
    + "org-mode file zettels",
    # add_completion=False,
)
console = Console(theme=custom_theme)


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(
            f"[yellow]zettelkasten[/] version: [bold blue]{__version__}[/]"
        )
        raise typer.Exit()


@app.callback()
def version(
    version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        # is_eager=True,
    ),
):
    """Prints the version of the package."""


def complete_zettel_name(incomplete: str):
    """Utility to propose zettelname completesion based on input."""
    completion = []
    for name in comp.parsed_zettels():
        if name.startswith(incomplete):
            completion.append(name)
    return completion


@app.command()
def add(
    zettel: str = typer.Argument(
        ...,
        autocompletion=complete_zettel_name,
    ),
    force_overwrite: bool = typer.Option(
        False,
        "-f",
        "--force_overwrite",
        help="Overwrite existing zettel. Use with extreme care!",
    ),
):
    """Adds a Zettel."""
    zadd.new_zettel(name=zettel, force_overwrite=force_overwrite)


# @app.command()
# def change():
#     """Change a Zettel"""
#     typer.echo("Change Zettel")


def print_colored_zettel(zettel, cmap):
    """Create a colored zettel list output according to the :ref:`colors`."""
    # decontruct zettel name
    parts = zettel.split(defaults.name_sep)

    colored_zettel = ""
    for i, part in enumerate(parts):
        if part in cmap:
            if i < len(parts) - 1:
                # add a name_sep it its not the first
                colored_zettel += (
                    f"[{cmap[part]}]{part}[/{cmap[part]}]{defaults.name_sep}"
                )
            else:
                colored_zettel += f"[{cmap[part]}]{part}[/{cmap[part]}]"
        else:
            if i < len(parts) - 1:
                colored_zettel += f"{part}{defaults.name_sep}"
            else:
                colored_zettel += part

    console.print(colored_zettel)


@app.command()
def list(
    category: str = typer.Option(
        None,
        "-c",
        "--cat",
        help="Only list zettels of this category",
    ),
    subcategory: str = typer.Option(
        None,
        "-s",
        "--subcat",
        help="Only list zettels of this subcategory",
    ),
):
    """List stored zettels."""
    # create a config parse able to parse lists
    configs = configparser.ConfigParser(
        converters={"list": lambda x: [i.strip() for i in x.split(",")]}
    )

    # read in the config styles file
    configs.read(defaults.styles_file)
    cmap = {k: v for k, v in configs["list_colors"].items()}

    lst = comp.parsed_zettels()
    # filter out cats/subcats if requested
    if category:
        lst = [e for e in lst if e.startswith(category)]
        if category in cmap:
            console.rule(f"[{cmap[category]}]{category}*/*")
        else:
            console.rule(f"[bold green]{category}*/*")
    if subcategory:
        subcat_str = f"{defaults.name_sep}{subcategory}{defaults.name_sep}"
        lst = [e for e in lst if subcat_str in e]
        if subcategory in cmap:
            console.rule(f"[{cmap[subcategory]}]*{subcat_str}*")
        else:
            console.rule(f"[bold green]*{subcat_str}*")

    console.print()
    for entry in lst:
        print_colored_zettel(entry, cmap)
    console.print()


@app.command()
def open(
    zettel: str = typer.Argument(
        ...,
        autocompletion=complete_zettel_name,
    ),
):
    """Opens a zettel if found inside zettelkasten."""
    zettel_path = parse.zettel_path(zettel).resolve()

    if platform.system() == "Darwin":  # macOS
        subprocess.call(("open", zettel_path))
    elif platform.system() == "Windows":  # Windows
        os.startfile(zettel_path)
    else:  # linux variants
        subprocess.call(("xdg-open", zettel_path))


@app.command()
def ref(
    zettel: str = typer.Argument(
        None,
        autocompletion=complete_zettel_name,
        help="Zettel as in 'category/subcategory/zettel' or 'zettel'.",
    ),
    source: str = typer.Argument(
        None,
        help="Path to source file as in '~/Documents/my_source_file.pdf'.",
    ),
    uid: str = typer.Argument(
        None,
        help="Unique reference identifier serving as bibtex key.",
    ),
    interactive: bool = typer.Option(
        False,
        "-i",
        "--interactive",
        help="Use interactive prompting instead of positional arguments.",
    ),
    location_specifier: str = typer.Option(
        None,
        "-loc",
        "-lc",
        "--location_specifier",
        help="Hint locating the exact reference inisde the source ('min 1').",
    ),
    author: str = typer.Option(
        None,
        "-a",
        "--author",
        help="Name of the author as in 'Surname, Name' or 'Name Surname'.",
    ),
    title: str = typer.Option(
        None,
        "-t",
        "--title",
        help="String specifying the reference file title.",
    ),
    year: str = typer.Option(
        None,
        "-y",
        "--year",
        help="Year the reference was 'published' as in 'YYYY'",
    ),
    date: str = typer.Option(
        None,
        "-d",
        "--date",
        help="Date the reference was 'published' as in 'YYYY-MM-DD'",
    ),
    force_overwrite: bool = typer.Option(
        False,
        "-f",
        "--force_overwrite",
        help="Overwrite the exisitng source file and bib entries.",
    ),
):
    """Adds a reference/source file to an existing zettel."""
    if zettel is None and interactive:
        zettel = Prompt.ask(
            "[b green]Zettel[/b green] the reference is added to"
        )

    if source is None and interactive:
        source = Prompt.ask(
            "[b green]Source[/b green] file serving as reference"
        )

    if uid is None and interactive:
        uid = Prompt.ask(
            "[b green]Unique identifier[/b green] of the reference file"
        )

    if interactive and location_specifier is None:
        location_specifier = Prompt.ask(
            "Specify where inside the file your reference is found",
            default=defaults.def_location_specifier,
        )

    if interactive and author is None:
        author = Prompt.ask(
            "[b cyan]Name[/b cyan] of the Author", default=defaults.def_author
        )

    if interactive and title is None:
        title = Prompt.ask(
            "[b cyan]Title[/b cyan] of the reference file",
            default=defaults.def_title,
        )

    if interactive and year is None:
        year = IntPrompt.ask(
            "[b cyan]Year[/b cyan] of the reference file",
            default=defaults.def_year,
        )

    if interactive and date is None:
        date = Prompt.ask(
            "[b cyan]Date[/b cyan] of the reference file",
            default=defaults.def_date,
        )

    # console.print(f"zettel: {zettel}")
    # console.print(f"source: {source}")
    # console.print(f"uid: {uid}")
    # console.print(f"locspec: {location_specifier}")
    # console.print(f"author: {author}")
    # console.print(f"title: {title}")
    # console.print(f"year: {year}")
    # console.print(f"date: {date}")

    zadd.new_source(
        zettel_name=zettel,
        source_file=source,
        uid=uid,
        locspec=location_specifier,
        author=author,
        title=title,
        year=year,
        date=date,
        force_overwrite=force_overwrite,
    )
