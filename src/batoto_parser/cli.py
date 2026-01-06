"""CLI interface for batoto-parser using Typer."""

import json
import sys
from typing import Optional
from urllib.parse import urljoin

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from batoto_parser import BatoToParser, MangaLoaderContext, Manga, __version__
from batoto_parser.utils import generate_uid

app = typer.Typer(
    name="batoto-parser",
    help="Lightweight parser for Batoto-style manga sites",
    add_completion=False,
)
console = Console()
error_console = Console(stderr=True)


def version_callback(value: bool):
    """Print version and exit."""
    if value:
        console.print(f"batoto-parser version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
):
    """
    Batoto Parser - Parse Batoto-style manga sites.
    
    Supports browsing, searching, fetching manga details, and chapter pages.
    """
    pass


def to_json(obj):
    """Convert objects to JSON with proper handling of dataclasses and sets."""
    def conv(o):
        if isinstance(o, set):
            return list(o)
        return o.__dict__ if hasattr(o, "__dict__") else str(o)
    return json.dumps(obj, default=conv, indent=2)


def make_min_manga(url: str, domain: str = "bato.si") -> Manga:
    """Create minimal Manga object from URL."""
    rel = url
    if url.startswith("http"):
        parsed = url.split(f"https://{domain}")[-1]
        rel = parsed or url
    
    return Manga(
        id=generate_uid(rel),
        title="",
        alt_titles=set(),
        url=rel,
        public_url=urljoin(f"https://{domain}", rel),
        cover_url=None,
        large_cover_url=None,
        description_html=None,
        tags=[],
        state=None,
        authors=set(),
        originalLanguage=None,
        translatedLanguage=None,
        originalWorkStatus=None,
        uploadStatus=None,
        yearOfRelease=None,
        chapterCount=0,
        chapters=[],
    )


@app.command(name="list")
def list_manga(
    page: int = typer.Option(1, "--page", "-p", help="Page number to fetch"),
    order: str = typer.Option("update.za", "--order", "-o", help="Sort order"),
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Search query"),
    domain: str = typer.Option("bato.si", "--domain", "-d", help="Domain to parse"),
    output: Optional[str] = typer.Option(None, "--output", "-O", help="Output file (default: stdout)"),
    pretty: bool = typer.Option(True, "--pretty/--compact", help="Pretty print JSON"),
):
    """
    List/browse manga from the site.
    
    Examples:
    
        batoto-parser list
        
        batoto-parser list --page 2
        
        batoto-parser list --query "one piece"
        
        batoto-parser list --page 1 --output results.json
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task(description="Fetching manga list...", total=None)
            
            ctx = MangaLoaderContext()
            parser = BatoToParser(ctx, domain=domain)
            mangas = parser.get_list(page=page, order=order, query=query)
        
        result = to_json(mangas) if pretty else json.dumps(mangas, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o))
        
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]✓[/green] Results saved to {output}")
        else:
            typer.echo(result)
            
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command(name="details")
def get_details(
    manga_url: str = typer.Argument(..., help="Manga URL or path (e.g., /series/Some-Manga)"),
    domain: str = typer.Option("bato.si", "--domain", "-d", help="Domain to parse"),
    output: Optional[str] = typer.Option(None, "--output", "-O", help="Output file (default: stdout)"),
    pretty: bool = typer.Option(True, "--pretty/--compact", help="Pretty print JSON"),
):
    """
    Get detailed information about a specific manga.
    
    Examples:
    
        batoto-parser details /series/Some-Manga
        
        batoto-parser details https://bato.si/series/Some-Manga
        
        batoto-parser details /series/Some-Manga --output manga.json
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task(description="Fetching manga details...", total=None)
            
            ctx = MangaLoaderContext()
            parser = BatoToParser(ctx, domain=domain)
            manga = make_min_manga(manga_url, domain=domain)
            details_data = parser.get_details(manga)
        
        result = to_json(details_data) if pretty else json.dumps(details_data, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o))
        
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]✓[/green] Details saved to {output}")
        else:
            typer.echo(result)
            
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command(name="pages")
def get_pages(
    chapter_url: str = typer.Argument(..., help="Chapter URL or path (e.g., /reader/12345)"),
    domain: str = typer.Option("bato.si", "--domain", "-d", help="Domain to parse"),
    output: Optional[str] = typer.Option(None, "--output", "-O", help="Output file (default: stdout)"),
    pretty: bool = typer.Option(True, "--pretty/--compact", help="Pretty print JSON"),
):
    """
    Get image URLs for a specific chapter.
    
    Requires Node.js installed on your system for JavaScript evaluation.
    
    Examples:
    
        batoto-parser pages /reader/12345
        
        batoto-parser pages /reader/12345 --output chapter.json
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task(description="Fetching chapter pages...", total=None)
            
            ctx = MangaLoaderContext()
            parser = BatoToParser(ctx, domain=domain)
            pages_data = parser.get_pages(chapter_url)
        
        result = to_json(pages_data) if pretty else json.dumps(pages_data, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o))
        
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]✓[/green] Pages saved to {output}")
        else:
            typer.echo(result)
            
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


def cli_main():
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    cli_main()