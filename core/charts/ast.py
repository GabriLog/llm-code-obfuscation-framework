import matplotlib.pyplot as plt
import numpy as np
from charts.save_fig import save_fig

SUBDIR = "charts"

def _label_bars(ax, bars, fmt="{:.2f}", offset=0.01):
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + offset,
                fmt.format(h),
                ha="center",
                va="bottom",
                fontsize=7
            )

def plot_ast(df, df_obf, df_deob):
    models = sorted(df["model"].dropna().unique())
    x = np.arange(len(models))
    width = 0.35

    df_llm = df_obf[df_obf["label"] == "obf_llm"]

    ast_obf = df_llm.groupby("model")["ast_score"].mean().reindex(models)
    ast_deob = df_deob.groupby("model")["ast_score"].mean().reindex(models)

    fig, ax = plt.subplots(figsize=(12, 5))
    fig.suptitle("AST Score (Obfuscated vs Deobfuscated) por Modelo", fontsize=13)

    b1 = ax.bar(x - width/2, ast_obf, width, label="AST Score Obf", color="steelblue")
    b2 = ax.bar(x + width/2, ast_deob, width, label="AST Score Deob", color="tomato")

    ax.set_ylabel("AST Score")
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=25)
    ax.set_ylim(0, 1.1)

    _label_bars(ax, b1)
    _label_bars(ax, b2)

    ax.legend(loc="upper right")

    plt.tight_layout()
    save_fig("ast_overview_by_model.png", SUBDIR)