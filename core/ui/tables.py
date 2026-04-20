from rich.console import Console
from rich.prompt import IntPrompt
from rich.table import Table
from rich import box

from core.domain.parsed_log import ParsedLog
from core.domain.eval_result import EvalResult
from core.ui.formatters import format_score, format_match, format_time

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


def print_results(parsed: ParsedLog, results: list[EvalResult]):
    title = (
        f"[bold]{parsed.model}[/bold] | "
        f"{parsed.strategy} | "
        f"{parsed.dataset} | "
        f"{parsed.script_name}"
    )
    console.print(f"\n{title}")
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("Resultado", style="bold")
    table.add_column("AST Score", justify="center")
    table.add_column("Nodos orig.", justify="right")
    table.add_column("Nodos result.", justify="right")
    table.add_column("Funcional", justify="center")
    table.add_column("Tiempo", justify="right")
    table.add_column("Error ejecución")

    for r in results:
        table.add_row(
            r.label,
            format_score(r.ast_score),
            str(r.ast_nodes_original),
            str(r.ast_nodes_result),
            format_match(r.functional_match),
            format_time(r.time_seconds),
            r.execution_error or "—",
        )
    console.print(table)
    obf_trad = next((r for r in results if r.label == "obf_tradicional"), None)
    obf_llm  = next((r for r in results if r.label == "obf_llm"), None)
    deob_llm = next((r for r in results if r.label == "deob_llm"), None)

    notes = []
    if obf_trad and obf_llm and obf_trad.ast_score and obf_llm.ast_score:
        if obf_trad.ast_score < obf_llm.ast_score:
            notes.append("→ Ofuscación tradicional altera más la estructura")
        else:
            notes.append("→ Ofuscación LLM altera más la estructura")

    if deob_llm:
        if deob_llm.functional_match:
            notes.append("→ Desofuscación LLM recupera correctamente la funcionalidad")
        else:
            notes.append("→ Desofuscación LLM NO recupera la funcionalidad original")

    for note in notes:
        console.print(f"[dim]{note}[/dim]")