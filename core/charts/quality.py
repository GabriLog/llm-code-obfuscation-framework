from charts.save_fig import save_fig
import matplotlib.pyplot as plt
import numpy as np

SUBDIR = "charts"

def plot_quality(df, df_obf):

    df_llm = df_obf[df_obf["label"] == "obf_llm"]
    df_trad = df_obf[df_obf["label"] == "obf_tradicional"]

    models = sorted(df_llm["model"].dropna().unique())
    x = np.arange(len(models))

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("Calidad de Ofuscación: AST Score, Node Ratio y Éxito Funcional", fontsize=13)

    metrics = [
        ("ast_score",        "AST Score",        True),
        ("node_ratio",       "Node Ratio",        False),
        ("functional_match", "Functional Match",  True),
    ]

    for ax, (metric, title, is_rate) in zip(axes, metrics):

        if metric == "ast_score":
            data = df_llm[df_llm["functional_match"] == True]
        else:
            data = df_llm

        vals_llm  = data.groupby("model")[metric].mean().reindex(models).fillna(0)
        val_trad  = df_trad[metric].mean()

        bar_labels = list(models) + ["obf_trad"]
        bar_values = list(vals_llm) + [val_trad]
        colors     = ["steelblue"] * len(models) + ["orange"]

        ax.bar(bar_labels, bar_values, color=colors, alpha=0.85)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Modelo / Método")
        ax.tick_params(axis="x", rotation=30)
        if is_rate:
            ax.set_ylim(0, 1)

        ax.text(len(models), val_trad + 0.02, f"{val_trad:.2f}", ha="center", fontsize=9)

    plt.tight_layout()
    save_fig("quality_overview_by_model.png", SUBDIR)