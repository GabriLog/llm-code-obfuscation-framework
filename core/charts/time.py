from charts.save_fig import save_fig
import matplotlib.pyplot as plt

SUBDIR = "time"

def plot_time(df, df_obf):

    plt.figure()
    df.groupby("model")["time_seconds"].mean().plot(kind="bar")
    plt.title("time_by_model_all")
    save_fig("by_model_all.png", SUBDIR)

    plt.figure()
    df_obf.groupby("model")["time_seconds"].mean().plot(kind="bar")
    plt.title("time_by_model_obf")
    save_fig("by_model_obf.png", SUBDIR)

    plt.figure()
    g = df.groupby("is_obfuscation")["time_seconds"].mean()
    g.index = ["Deobf", "Obf"]
    g.plot(kind="bar")
    plt.title("time_general_task")
    save_fig("general_task.png", SUBDIR)

    plt.figure()
    df.groupby("strategy")["time_seconds"].mean().plot(kind="bar")
    plt.title("time_by_strategy")
    save_fig("by_strategy.png", SUBDIR)

    g = df_obf.groupby("label")["time_seconds"].mean()
    ratio = g["obf_llm"] / g["obf_tradicional"]
    plt.figure()
    plt.bar(["LLM / Trad"], [ratio])
    plt.title("time_ratio_llm_vs_trad")
    save_fig("ratio_llm_vs_trad.png", SUBDIR)

    plt.figure()
    df_obf.groupby(["dataset", "label"])["time_seconds"].mean().unstack().plot(kind="bar")
    plt.title("time_by_dataset")
    save_fig("by_dataset.png", SUBDIR)

    plt.figure()
    for label in ["obf_tradicional", "obf_llm"]:
        subset = df_obf[df_obf["label"] == label]
        plt.scatter(subset["time_seconds"], subset["ast_score"], label=label, alpha=0.6)
    plt.legend()
    plt.title("scatter_time_vs_ast")
    save_fig("scatter_time_vs_ast.png", SUBDIR)