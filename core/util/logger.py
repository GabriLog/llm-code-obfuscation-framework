from pathlib import Path
from datetime import datetime
import re

def clean_llm_output(text: str) -> str:
    match = re.search(r"```(?:javascript)?\s*(.*?)```", text, re.DOTALL)
    if match:
        text = match.group(1)
    text = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r'(?<!:)//.*', '', text)

    return text.strip()

def log_experiment(experiment, obf_time, llm_time, deob_time, obf_result, llm_result, deob_result):
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"experiment_{timestamp}.txt"

    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"Experiment Timestamp: {datetime.now()}\n")
        f.write("\n--- Experiment Summary ---\n")
        f.write(f"Model: {experiment.model}\n")
        f.write(f"Strategy: {experiment.strategy}\n")
        f.write(f"Dataset: {experiment.dataset}\n")
        f.write(f"Script: {experiment.script_name}\n")

        f.write("\n--- Obfuscation Traditional ---\n")
        f.write(f"Time: {obf_time:.2f}s\n")
        f.write(f"Result:\n{obf_result}\n")

        f.write("\n--- Obfuscation LLM ---\n")
        f.write(f"Time: {llm_time:.2f}s\n")
        f.write(f"Result:\n{llm_result}\n")

        f.write("\n--- Deobfuscation LLM ---\n")
        f.write(f"Time: {deob_time:.2f}s\n")
        f.write(f"Result:\n{deob_result}\n")

