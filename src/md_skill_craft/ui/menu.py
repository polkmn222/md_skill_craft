"""Interactive menu system."""

from typing import List, Tuple, Callable, Any
from rich.console import Console
from rich.prompt import Prompt as RichPrompt

console = Console()


class Menu:
    """Interactive numbered menu system."""

    @staticmethod
    def select(
        prompt: str,
        options: List[Tuple[int, str, str | None] | Tuple[int, str]] = None,
        descriptions: List[str] | None = None,
    ) -> int:
        """Show numbered menu and get selection.

        Args:
            prompt: Menu prompt text
            options: List of (number, label) or (number, label, description) tuples
            descriptions: Optional list of descriptions to show above options

        Returns:
            Selected option number
        """
        console.print(f"\n{prompt}")

        if descriptions:
            for desc in descriptions:
                console.print(f"[dim]{desc}[/dim]")

        if options:
            for opt in options:
                num = opt[0]
                label = opt[1]
                description = opt[2] if len(opt) > 2 else None

                if description:
                    console.print(f"  [cyan][{num}][/cyan] {label} — [dim]{description}[/dim]")
                else:
                    console.print(f"  [cyan][{num}][/cyan] {label}")

            numbers = [opt[0] for opt in options]
        else:
            raise ValueError("Options list cannot be empty")

        while True:
            try:
                choice = RichPrompt.ask("[green]> [/green]", console=console)
                choice_num = int(choice)

                if choice_num in numbers:
                    return choice_num
                else:
                    console.print(f"[red]❌ Invalid selection. Please choose from {numbers}.[/red]")
            except ValueError:
                console.print(f"[red]❌ Please enter a number.[/red]")

    @staticmethod
    def select_multiple(
        prompt: str,
        options: List[Tuple[int, str, str | None] | Tuple[int, str]] = None,
    ) -> List[int]:
        """Show menu for multiple selections (comma-separated).

        Args:
            prompt: Menu prompt text
            options: List of (number, label) or (number, label, description) tuples

        Returns:
            List of selected option numbers
        """
        console.print(f"\n{prompt} [dim](comma-separated)[/dim]")

        if options:
            for opt in options:
                num = opt[0]
                label = opt[1]
                description = opt[2] if len(opt) > 2 else None

                if description:
                    console.print(f"  [cyan][{num}][/cyan] {label} — [dim]{description}[/dim]")
                else:
                    console.print(f"  [cyan][{num}][/cyan] {label}")

            numbers = [opt[0] for opt in options]
        else:
            raise ValueError("Options list cannot be empty")

        while True:
            try:
                choice = RichPrompt.ask("[green]> [/green]", console=console)
                choices = [int(x.strip()) for x in choice.split(",")]

                if all(c in numbers for c in choices):
                    return choices
                else:
                    console.print(f"[red]❌ Invalid selection.[/red]")
            except ValueError:
                console.print(f"[red]❌ Please enter numbers separated by commas.[/red]")

    @staticmethod
    def confirm(prompt: str, default: bool = True) -> bool:
        """Show yes/no confirmation.

        Args:
            prompt: Confirmation prompt
            default: Default value if user just presses Enter

        Returns:
            True for yes, False for no
        """
        default_str = "[Y/n]" if default else "[y/N]"
        while True:
            response = RichPrompt.ask(f"\n{prompt} {default_str}", console=console).lower().strip()

            if not response:
                return default
            elif response in ("y", "yes"):
                return True
            elif response in ("n", "no"):
                return False
            else:
                console.print("[red]❌ Please enter y or n.[/red]")

    @staticmethod
    def prompt(
        prompt_text: str,
        default: str | None = None,
        validate_fn: Callable[[str], bool] | None = None,
    ) -> str:
        """Show text input prompt.

        Args:
            prompt_text: Prompt text
            default: Default value
            validate_fn: Optional validation function

        Returns:
            User input
        """
        while True:
            response = RichPrompt.ask(f"\n{prompt_text}", default=default, console=console)

            if validate_fn and not validate_fn(response):
                console.print("[red]❌ Invalid input.[/red]")
                continue

            return response
