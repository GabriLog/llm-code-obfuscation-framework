from core.util.ollama_client import list_models
from core.ui.tables import select_option
from pathlib import Path

DATASETS_PATH = Path("datasets")


def select_model():
    return select_option(list_models(), "Modelo")

def select_strategy():
    return select_option(["zero-shot", "few-shot"], "Estrategia")

def select_dataset():
    return select_option(["small", "large"], "Dataset")

def select_script(dataset):
    folder = DATASETS_PATH / "original" / dataset
    scripts = [f.name for f in folder.glob("*.js")]
    return select_option(scripts, "Script")

def read_script(script_name, dataset):
    path = DATASETS_PATH / "original" / dataset / script_name
    return path.read_text(encoding="utf-8")
