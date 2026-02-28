from rich.console import Console
from core.ui.live_timer import LiveTimer
from core.ui.panels import show_banner, show_experiment_summary, show_result, show_time
from core.util.logger import log_experiment
from core import build_experiment, load_prompt
from runs import run_baseline, run_llm
import time

console = Console()


def main():
    # Bienvenida
    console.clear()
    show_banner()

    # Configuración experimento
    experiment = build_experiment()
    show_experiment_summary(experiment)
    prompt = load_prompt(experiment)

    # Ofuscación tradicional
    obfuscation_time = run_baseline(experiment)
    show_time(obfuscation_time)

    from pathlib import Path
    output_path = Path("datasets/obfuscation") / experiment.dataset / experiment.script_name
    obf_result = output_path.read_text(encoding="utf-8")
    show_result(obf_result)

    # Ofuscación LLM
    print("\n==== PROMPT OFUSCACIÓN ====\n")
    print(prompt.format(code=experiment.script))
    print("\n===========================\n")

    start = time.perf_counter()
    with LiveTimer(console):
        llm_result = run_llm(
            experiment.model,
            prompt,
            experiment.script,
        )
    llm_time = time.perf_counter() - start
    show_result(llm_result)

    # Modo desofuscación
    experiment.task = "desofuscar"
    experiment.script = output_path.read_text(encoding="utf-8")
    prompt = load_prompt(experiment)

    # Desofuscación LLM 
    print("\n==== PROMPT DESOFUSCACIÓN ====\n")
    print(prompt.format(code=experiment.script))
    print("\n==============================\n")

    start = time.perf_counter()
    with LiveTimer(console):
        deob_result = run_llm(
            experiment.model,
            prompt,
            experiment.script,
        )
    deob_time = time.perf_counter() - start
    show_result(deob_result)

    log_experiment(
        experiment,
        obfuscation_time,
        llm_time,
        deob_time,
        obf_result,
        llm_result,
        deob_result,
    )


if __name__ == "__main__":
    main()
