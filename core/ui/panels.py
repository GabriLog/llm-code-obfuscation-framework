from core.domain.experiment_config import ExperimentConfig
from rich.console import Console
from rich.panel import Panel

console = Console()


def show_banner():
    console.print("\n", Panel.fit(
            "[bold magenta]LLM Code Obfuscation Lab[/bold magenta]\n"
            "Evaluación del potencial de los LLMs en tareas\n"
            "de ofuscación y desofuscación de código",
            border_style="magenta"
        )
    )

def show_experiment_summary(exp: ExperimentConfig):
    console.print("\n", Panel.fit(
        f"[bold]Resumen del experimento[/bold]\n\n"
        f"• Modelo: [bold green]{exp.model}[/bold green]\n"
        f"• Estrategia: [bold green]{exp.strategy}[/bold green]\n"
        f"• Dataset: [bold green]{exp.dataset}[/bold green]\n"
        f"• Script: [bold green]{exp.script_name}[/bold green]",
        border_style="green"
    ))

def show_time(time):
    console.print("\n", Panel(
            f"⏳ Ofuscador tradicional: {time}s",
            style="yellow"
        )
    )

def show_result(result):
    console.print("\n", Panel(
            result,
            title="Resultado",
            border_style="green"
        )
    )
