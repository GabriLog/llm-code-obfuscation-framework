from charts.save_fig import save_fig
import matplotlib.pyplot as plt
import numpy as np

SUBDIR = "charts"

def _label_bars(ax, bars, fmt="{:.2f}", offset=0.01):
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + offset,
                    fmt.format(h), ha="center", va="bottom", fontsize=7)

def plot_error(df, df_obf, df_deob):
    models = sorted(df["model"].dropna().unique())
    x = np.arange(len(models))
    width = 0.3

    df_trad = df[df["label"] == "obf_tradicional"]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("Tasa de Error y Éxito Funcional por Modelo", fontsize=13)

    for ax, metric, title in [
        (axes[0], "is_error",         "Tasa de Error (LLM)"),
        (axes[1], "functional_match", "Éxito Funcional (LLM)"),
    ]:
        for i, (lbl, color) in enumerate(zip(["obf_llm", "deob_llm"], ["orange", "tomato"])):
            subset = df[df["label"] == lbl]
            vals = subset.groupby("model")[metric].mean().reindex(models).fillna(0)
            bars = ax.bar(x + (i - 0.5) * width, vals, width, label=lbl, color=color, alpha=0.85)
            _label_bars(ax, bars)
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=25)
        ax.set_ylim(0, 1.1)
        ax.legend()

    error_mean = df_trad["is_error"].mean()
    func_mean  = df_trad["functional_match"].mean()
    bars = axes[2].bar(["Error Rate", "Functional Match"], [error_mean, func_mean],
                       color=["crimson", "steelblue"], alpha=0.85, width=0.4)
    axes[2].set_title("Ofuscador Tradicional (Media Global)")
    axes[2].set_ylim(0, 1.1)
    axes[2].set_ylabel("Valor medio")
    _label_bars(axes[2], bars, offset=0.02)

    plt.tight_layout()
    save_fig("error_and_functional_by_model.png", SUBDIR)