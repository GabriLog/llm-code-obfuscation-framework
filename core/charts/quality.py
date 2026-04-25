from charts.save_fig import save_fig
import matplotlib.pyplot as plt
import numpy as np

SUBDIR = "charts"

def _label_bars(ax, bar_labels, bar_values, fmt="{:.2f}", offset=0.02):
    for i, v in enumerate(bar_values):
        if v is not None and not (isinstance(v, float) and np.isnan(v)):
            ax.text(i, v + offset, fmt.format(v), ha="center", va="bottom", fontsize=8)

def plot_quality(df, df_obf):
    df_llm  = df_obf[df_obf["label"] == "obf_llm"]
    df_trad = df_obf[df_obf["label"] == "obf_tradicional"]

    models = sorted(df_llm["model"].dropna().unique())

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("Calidad de Ofuscación: AST Score, Node Ratio y Éxito Funcional", fontsize=13)

    metrics = [
        ("ast_score",        "AST Score (obf_llm)",       True,  df_llm),
        ("node_ratio",       "Node Ratio (obf_llm)",      False, df_llm),
        ("functional_match", "Functional Match",          True,  df_llm),
    ]

    for ax, (metric, title, is_rate, source) in zip(axes, metrics):

        data = source

        vals_llm = data.groupby("model")[metric].mean().reindex(models).fillna(0)
        val_trad = df_trad[metric].mean()

        bar_labels = list(models) + ["obf_trad"]
        bar_values = list(vals_llm.values) + [val_trad]
        colors     = ["steelblue"] * len(models) + ["orange"]

        ax.bar(bar_labels, bar_values, color=colors, alpha=0.85)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Modelo / Método")
        ax.tick_params(axis="x", rotation=30)
        if is_rate:
            ax.set_ylim(0, 1.1)

        _label_bars(ax, bar_labels, bar_values)

    plt.tight_layout()
    save_fig("quality_overview_by_model.png", SUBDIR)