from charts.save_fig import save_fig
import matplotlib.pyplot as plt
import numpy as np

SUBDIR = "charts"

MODEL_COLORS = {
    "llama3.2:3b":        "#4C72B0",   # azul
    "qwen2.5-coder:7b":   "#DD8452",   # naranja
    "mistral:7b":         "#55A868",   # verde
    "llama3.1:8b":        "#C44E52",   # rojo
}
DEFAULT_COLOR = "#8C8C8C"


def get_model_color(model: str) -> str:
    return MODEL_COLORS.get(model, DEFAULT_COLOR)


def _label_bars(ax, bars, fmt="{:.1f}s", offset=0.5):
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2, h + offset,
                fmt.format(h), ha="center", va="bottom", fontsize=7
            )


def plot_time(df, df_obf):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Tiempo de Ejecución por Modelo y Relación con Calidad AST", fontsize=13)

    models = sorted(df["model"].dropna().unique())
    x = np.arange(len(models))
    width = 0.25
    task_labels = ["obf_tradicional", "obf_llm", "deob_llm"]
    task_hatches = ["", "//", ".."]   # hatch por tarea, color por modelo

    for i, (lbl, hatch) in enumerate(zip(task_labels, task_hatches)):
        subset = df[df["label"] == lbl]
        vals = subset.groupby("model")["time_seconds"].mean().reindex(models).fillna(0)
        for j, (model, val) in enumerate(zip(models, vals)):
            bar = axes[0].bar(
                x[j] + (i - 1) * width, val, width,
                color=get_model_color(model),
                hatch=hatch,
                alpha=0.85,
                label=f"{model}" if i == 0 else "_nolegend_",
            )
            _label_bars(axes[0], bar)

    axes[0].legend(title="Modelo", loc="upper left", fontsize=8)

    from matplotlib.patches import Patch
    hatch_legend = [
        Patch(facecolor="white", edgecolor="black", hatch=h, label=lbl)
        for lbl, h in zip(task_labels, task_hatches)
    ]
    axes[0].legend(
        handles=axes[0].get_legend_handles_labels()[0] + hatch_legend,
        labels=axes[0].get_legend_handles_labels()[1] + task_labels,
        title="Modelo / Tarea", loc="upper left", fontsize=7
    )

    axes[0].set_title("Tiempo Medio por Modelo y Tarea")
    axes[0].set_ylabel("Segundos")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(models, rotation=25)

    for model in models:
        subset = df_obf[df_obf["model"] == model]
        axes[1].scatter(
            subset["time_seconds"], subset["ast_score"],
            label=model, color=get_model_color(model),
            alpha=0.6, s=40
        )

    axes[1].set_title("Tiempo vs AST Score (Ofuscación)")
    axes[1].set_xlabel("Tiempo (s)")
    axes[1].set_ylabel("AST Score")
    axes[1].legend(title="Modelo", fontsize=8)

    plt.tight_layout()
    save_fig("time_overview.png", SUBDIR)