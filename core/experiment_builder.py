from core.domain.experiment_config import ExperimentConfig
from core.util.setup_helpers import (
    select_model,
    select_dataset,
    select_script,
    read_script,
    select_strategy,
)


def build_experiment() -> ExperimentConfig:
    model = select_model()
    task = "ofuscar"
    strategy = select_strategy()

    dataset = select_dataset()
    script_name = select_script(dataset)
    script = read_script(script_name, dataset)

    return ExperimentConfig(
        model=model,
        task=task,
        strategy=strategy,
        dataset=dataset,
        script_name=script_name,
        script=script,
    )
