from dataclasses import dataclass

@dataclass
class ExperimentConfig:
    model: str
    task: str
    strategy: str
    dataset: str
    script_name: str
    script: str
