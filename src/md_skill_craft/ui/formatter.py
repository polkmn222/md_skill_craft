"""Terminal formatting utilities using Rich."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def print_header(title: str, subtitle: str = "") -> None:
    """Print a formatted header.

    Args:
        title: Header title
        subtitle: Optional subtitle
    """
    content = f"[bold]{title}[/bold]"
    if subtitle:
        content += f"\n[dim]{subtitle}[/dim]"

    panel = Panel(
        content,
        style="cyan",
        expand=False,
    )
    console.print(panel)


def print_section(title: str) -> None:
    """Print a section divider.

    Args:
        title: Section title
    """
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    console.print("[dim]" + "─" * 60 + "[/dim]")


def print_success(message: str) -> None:
    """Print a success message.

    Args:
        message: Message to print
    """
    console.print(f"[green]✅ {message}[/green]")


def print_warning(message: str) -> None:
    """Print a warning message.

    Args:
        message: Message to print
    """
    console.print(f"[yellow]⚠️  {message}[/yellow]")


def print_error(message: str) -> None:
    """Print an error message.

    Args:
        message: Message to print
    """
    console.print(f"[red]❌ {message}[/red]")


def print_info(message: str) -> None:
    """Print an info message.

    Args:
        message: Message to print
    """
    console.print(f"[blue]ℹ️  {message}[/blue]")


def print_option(number: int, text: str, description: str = "") -> None:
    """Print a numbered option.

    Args:
        number: Option number
        text: Option text
        description: Optional description
    """
    output = f"  [cyan][{number}][/cyan] {text}"
    if description:
        output += f" — [dim]{description}[/dim]"
    console.print(output)


def print_code_block(code: str, title: str = "") -> None:
    """Print a code block.

    Args:
        code: Code to display
        title: Optional title for the block
    """
    if title:
        console.print(f"\n[dim]{title}[/dim]")
    console.print("[dim]" + "─" * 60 + "[/dim]")
    console.print(code)
    console.print("[dim]" + "─" * 60 + "[/dim]\n")


def print_table_row(columns: list[str], is_header: bool = False) -> None:
    """Print a table row.

    Args:
        columns: Column values
        is_header: Whether this is a header row
    """
    if is_header:
        formatted = " | ".join(f"[bold]{col}[/bold]" for col in columns)
        console.print(formatted)
        console.print("[dim]" + "─" * 60 + "[/dim]")
    else:
        console.print(" | ".join(columns))
