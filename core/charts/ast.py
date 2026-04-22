from charts.save_fig import save_fig
import matplotlib.pyplot as plt

SUBDIR = "ast"

def plot_ast(df, df_obf, df_deob):

    plt.figure()
    df_obf.groupby("model")["ast_score"].mean().plot(kind="bar")
    plt.title("ast_by_model_obf")
    save_fig("by_model_obf.png", SUBDIR)

    plt.figure()
    df_deob.groupby("model")["ast_score"].mean().plot(kind="bar")
    plt.title("ast_by_model_deobf")
    save_fig("by_model_deobf.png", SUBDIR)

    plt.figure()
    df_obf.groupby("strategy")["ast_score"].mean().plot(kind="bar")
    plt.title("ast_by_strategy_obf")
    save_fig("by_strategy_obf.png", SUBDIR)

    plt.figure()
    df_deob.groupby("strategy")["ast_score"].mean().plot(kind="bar")
    plt.title("ast_by_strategy_deobf")
    save_fig("by_strategy_deobf.png", SUBDIR)