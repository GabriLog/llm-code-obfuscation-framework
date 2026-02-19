from rich.console import Console
from core.ui.live_timer import LiveTimer
from core.ui.panels import show_banner, show_experiment_summary, show_result, show_time
from core import build_experiment, load_prompt
from runs import run_baseline, run_llm

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

    with LiveTimer(console):
        llm_result = run_llm(
            experiment.model,
            prompt,
            experiment.script,
        )
    show_result(llm_result)

    # Modo desofuscación
    experiment.task = "desofuscar"
    experiment.script = llm_result
    prompt = load_prompt(experiment)

    # Desofuscación LLM 
    print("\n==== PROMPT DESOFUSCACIÓN ====\n")
    print(prompt.format(code=experiment.script))
    print("\n==============================\n")

    with LiveTimer(console):
        deob_result = run_llm(
            experiment.model,
            prompt,
            experiment.script,
        )
    show_result(deob_result)


if __name__ == "__main__":
    main()
