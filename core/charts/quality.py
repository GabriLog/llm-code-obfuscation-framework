from charts.save_fig import save_fig
import matplotlib.pyplot as plt

SUBDIR = "quality"

def plot_quality(df, df_obf):

    plt.figure()
    df_obf[df_obf["functional_match"]] \
        .groupby("label")["ast_score"].mean().plot(kind="bar")
    plt.title("ast_only_functional")
    save_fig("ast_only_functional.png", SUBDIR)

    df["node_ratio"] = df["ast_nodes_result"] / df["ast_nodes_original"]
    df.loc[df["ast_nodes_original"] == 0, "node_ratio"] = None
    plt.figure()
    df_obf.groupby("label")["node_ratio"].mean().plot(kind="bar")
    plt.title("node_ratio")
    save_fig("node_ratio.png", SUBDIR)

    plt.figure()
    for label in ["obf_tradicional", "obf_llm"]:
        subset = df_obf[df_obf["label"] == label]
        plt.scatter(subset["node_ratio"], subset["ast_score"], label=label, alpha=0.6)
    plt.legend()
    plt.title("scatter_ast_vs_node_ratio")
    save_fig("scatter_ast_vs_node_ratio.png", SUBDIR)

    g_time = df_obf.groupby("label")["time_seconds"].mean()
    g_func = df_obf.groupby("label")["functional_match"].mean()
    fig, ax1 = plt.subplots()
    ax1.bar(g_time.index, g_time.values)
    ax2 = ax1.twinx()
    ax2.plot(g_func.index, g_func.values, marker='o')
    plt.title("time_vs_success")
    save_fig("time_vs_success.png", SUBDIR)