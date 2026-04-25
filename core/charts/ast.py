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

def plot_ast(df, df_obf, df_deob):
    models = sorted(df["model"].dropna().unique())
    x = np.arange(len(models))
    width = 0.25

    df_llm = df_obf[df_obf["label"] == "obf_llm"] 
    ast_obf    = df_llm.groupby("model")["ast_score"].mean().reindex(models)
    ast_deob   = df_deob.groupby("model")["ast_score"].mean().reindex(models)
    node_ratio = df_llm.groupby("model")["node_ratio"].mean().reindex(models)

    fig, ax1 = plt.subplots(figsize=(12, 5))
    fig.suptitle("AST Score (Obf / Deob) y Node Ratio por Modelo", fontsize=13)

    ax2 = ax1.twinx()
    b0 = ax2.bar(x - width, node_ratio, width, label="Node Ratio (Obf)", color="orange", alpha=0.75)
    ax2.set_ylabel("Node Ratio")
    _label_bars(ax2, b0, fmt="{:.2f}")

    b1 = ax1.bar(x,         ast_obf,  width, label="AST Score Obf",  color="steelblue")
    b2 = ax1.bar(x + width, ast_deob, width, label="AST Score Deob", color="tomato")
    ax1.set_ylabel("AST Score")
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, rotation=25)
    ax1.set_ylim(0, 1.1)
    _label_bars(ax1, b1)
    _label_bars(ax1, b2)

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h2 + h1, l2 + l1, loc="upper right")

    plt.tight_layout()
    save_fig("ast_overview_by_model.png", SUBDIR)