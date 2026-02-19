from rich.console import Console
from rich.prompt import IntPrompt
from rich.table import Table

console = Console()


def select_option(options, column):
    table = Table(title=column+"s disponibles", show_lines=True)
    table.add_column("#", justify="center")
    table.add_column(column, style="bright_cyan")

    for i, item in enumerate(options, 1):
        table.add_row(str(i), str(item))

    console.print("\n", table)
    choice = IntPrompt.ask(
        "Selecciona una opción",
        choices=[str(i) for i in range(1, len(options) + 1)]
    )
    selected = options[int(choice) - 1]
    return selected.split()[0]
