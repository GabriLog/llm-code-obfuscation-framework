from charts.save_fig import save_fig
import matplotlib.pyplot as plt
import numpy as np

SUBDIR = "charts"

def plot_time(df, df_obf):

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Tiempo de Ejecución por Modelo y Relación con Calidad AST", fontsize=13)

    models = sorted(df["model"].dropna().unique())
    x = np.arange(len(models))
    width = 0.25
    task_labels = ["obf_tradicional", "obf_llm", "deob_llm"]
    colors = ["steelblue", "orange", "tomato"]

    for i, (lbl, color) in enumerate(zip(task_labels, colors)):
        subset = df[df["label"] == lbl]
        vals = subset.groupby("model")["time_seconds"].mean().reindex(models).fillna(0)
        axes[0].bar(x + (i - 1) * width, vals, width, label=lbl, color=color, alpha=0.85)

    axes[0].set_title("Tiempo Medio por Modelo y Tarea")
    axes[0].set_ylabel("Segundos")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(models, rotation=25)
    axes[0].legend()

    colors_scatter = {"obf_tradicional": "steelblue", "obf_llm": "orange"}
    for lbl, color in colors_scatter.items():
        subset = df_obf[df_obf["label"] == lbl]
        axes[1].scatter(subset["time_seconds"], subset["ast_score"],
                        label=lbl, color=color, alpha=0.6)
    axes[1].set_title("Tiempo vs AST Score (Ofuscación)")
    axes[1].set_xlabel("Tiempo (s)")
    axes[1].set_ylabel("AST Score")
    axes[1].legend()

    plt.tight_layout()
    save_fig("time_overview.png", SUBDIR)