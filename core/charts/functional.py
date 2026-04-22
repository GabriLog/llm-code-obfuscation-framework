from charts.save_fig import save_fig
import matplotlib.pyplot as plt

SUBDIR = "functional"

def plot_functional(df, df_obf, df_deob):

    plt.figure()
    df.groupby("model")["functional_match"].mean().plot(kind="bar")
    plt.title("functional_by_model_all")
    save_fig("by_model_all.png", SUBDIR, True)

    plt.figure()
    df_obf.groupby("model")["functional_match"].mean().plot(kind="bar")
    plt.title("functional_by_model_obf")
    save_fig("by_model_obf.png", SUBDIR, True)

    plt.figure()
    df_deob.groupby("model")["functional_match"].mean().plot(kind="bar")
    plt.title("functional_by_model_deobf")
    save_fig("by_model_deobf.png", SUBDIR, True)

    plt.figure()
    g = df.groupby("is_obfuscation")["functional_match"].mean()
    g.index = ["Deobf", "Obf"]
    g.plot(kind="bar")
    plt.title("functional_general_task")
    save_fig("general_task.png", SUBDIR, True)

    plt.figure()
    df.groupby("strategy")["functional_match"].mean().plot(kind="bar")
    plt.title("functional_by_strategy")
    save_fig("by_strategy.png", SUBDIR, True)