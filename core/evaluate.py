import json
from pathlib import Path
from rich.console import Console
import subprocess
import sys

from core.ui.tables import print_results
from core.domain.parsed_log import ParsedLog
from core.util.log_parser import parse_log
from runs.evaluation.run_evaluator import evaluate_experiment

console = Console()

DATASETS_ORIGINAL = Path("datasets/original")


def get_original_code(parsed: ParsedLog) -> str | None:
    path = DATASETS_ORIGINAL / parsed.dataset / parsed.script_name
    if path.exists():
        return path.read_text(encoding="utf-8")
    return None


def evaluate_log(log_path: str) -> dict:
    parsed = parse_log(log_path)
    original_code = get_original_code(parsed)
    if original_code is None:
        console.print(
            f"[red]No se encontró el script original para: "
            f"{parsed.script_name} ({parsed.dataset})[/red]"
        )
        return {"error": "original_not_found", "log": log_path}

    with console.status(f"Evaluando {Path(log_path).name}..."):
        results = evaluate_experiment(
            original_code=original_code,
            obf_traditional=parsed.obf_traditional,
            obf_llm=parsed.obf_llm,
            deob_llm=parsed.deob_llm,
            time_obf_traditional=parsed.time_obf_traditional,
            time_obf_llm=parsed.time_obf_llm,
            time_deob_llm=parsed.time_deob_llm,
        )
    print_results(parsed, results)
    return {
        "timestamp": parsed.timestamp,
        "model": parsed.model,
        "strategy": parsed.strategy,
        "dataset": parsed.dataset,
        "script": parsed.script_name,
        "results": [r.to_dict() for r in results],
    }


def main():
    console.rule("[bold cyan]Evaluación de experimentos[/bold cyan]")
    logs_dir = Path("logs")
    out_path = Path("outputs/resultados.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    log_files = sorted(logs_dir.rglob("*.txt"))
    if not log_files:
        console.print(f"[yellow]No se encontraron logs .txt en {logs_dir}[/yellow]")
        return
    console.print(f"[dim]Encontrados {len(log_files)} logs en {logs_dir}[/dim]")

    all_results = []
    for lf in log_files:
        all_results.append(evaluate_log(str(lf)))

    out_path.write_text(
        json.dumps(all_results, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    console.print(f"\n[green]Resultados guardados en {out_path}[/green]")
    console.rule()

    console.print("[dim]Ejecutando chart_analysis.py...[/dim]")

    script_path = Path(__file__).parent / "chart_analysis.py"

    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
        console.print("[green]chart_analysis.py ejecutado correctamente[/green]")
    except subprocess.CalledProcessError:
        console.print("[red]Error al ejecutar chart_analysis.py[/red]")


if __name__ == "__main__":
    main()