from rich.console import Console
from rich.theme import Theme

# Console setup
console = Console(theme=Theme({
    "success": "green",
    "error": "red",
    "info": "blue",
    "warning": "yellow"
}))

# Emojis constants
EMOJIS = {
    "rocket": "🚀",
    "check": "✅",
    "key": "🔑",
    "error": "❌",
    "warning": "⚠️"
}

def print_success(message: str) -> None:
    """Print a success message with emoji."""
    console.print(f"{EMOJIS['check']} [success]{message}[/]")

def print_error(message: str) -> None:
    """Print an error message with emoji."""
    console.print(f"{EMOJIS['error']} [error]{message}[/]")

def print_info(message: str) -> None:
    """Print an info message with emoji."""
    console.print(f"{EMOJIS['rocket']} [info]{message}[/]")

def print_warning(message: str) -> None:
    """Print a warning message with emoji."""
    console.print(f"{EMOJIS['warning']} [warning]{message}[/]") 