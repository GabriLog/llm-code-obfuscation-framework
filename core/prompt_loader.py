from core.experiment_config import ExperimentConfig
from pathlib import Path
import json
from core.prompt_builder import (
    build_zeroshot,
    build_fewshot,
    load_examples,
)

PROMPTS_PATH = Path("prompts_config.json")

with PROMPTS_PATH.open(encoding="utf-8") as f:
    PROMPTS = json.load(f)

    
def load_prompt(experiment: ExperimentConfig):
    prompt_path = PROMPTS[experiment.model][experiment.task]
    base_prompt = Path(prompt_path).read_text(encoding="utf-8")

    if experiment.strategy == "zero-shot":
        return build_zeroshot(base_prompt)

    if experiment.strategy == "few-shot":
        examples = load_examples(
            experiment.dataset,
            experiment.script_name,
            experiment.task,
        )
        return build_fewshot(base_prompt, examples)

    raise ValueError(f"Unknown strategy: {experiment.strategy}")

