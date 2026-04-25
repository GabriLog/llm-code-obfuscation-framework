from charts.save_fig import save_fig
import matplotlib.pyplot as plt

SUBDIR = "charts"

def plot_functional(df, df_obf, df_deob):

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Impacto de la Estrategia (Zero-shot vs Few-shot)", fontsize=13)

    for ax, metric, title, ylabel in [
        (axes[0], "functional_match", "Éxito Funcional por Estrategia", "functional match"),
        (axes[1], "is_error",         "Tasa de Error por Estrategia",   "tasa de error"),
    ]:
        pivot = df.pivot_table(
            index="strategy", columns="label", values=metric, aggfunc="mean"
        )
        pivot.plot(kind="bar", ax=ax)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlabel("Estrategia")
        ax.set_ylim(0, 1)
        ax.tick_params(axis="x", rotation=15)
        ax.legend(title="Label", fontsize=8)

    plt.tight_layout()
    save_fig("strategy_functional_vs_error.png", SUBDIR)