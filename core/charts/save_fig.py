import matplotlib.pyplot as plt
from pathlib import Path

BASE_OUTPUT_DIR = Path("outputs")
BASE_OUTPUT_DIR.mkdir(exist_ok=True)

def save_fig(name, subfolder=None, force_unit=False):
    if force_unit:
        plt.ylim(0, 1)

    output_dir = BASE_OUTPUT_DIR
    if subfolder:
        output_dir = BASE_OUTPUT_DIR / subfolder
        output_dir.mkdir(parents=True, exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_dir / name, dpi=300)
    plt.close()