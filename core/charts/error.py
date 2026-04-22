from charts.save_fig import save_fig
import matplotlib.pyplot as plt

SUBDIR = "error"

def plot_error(df, df_obf, df_deob):

    plt.figure()
    df.groupby("model")["is_error"].mean().plot(kind="bar")
    plt.title("error_by_model_all")
    save_fig("by_model_all.png", SUBDIR, True)

    plt.figure()
    df_obf.groupby("model")["is_error"].mean().plot(kind="bar")
    plt.title("error_by_model_obf")
    save_fig("by_model_obf.png", SUBDIR, True)

    plt.figure()
    df_deob.groupby("model")["is_error"].mean().plot(kind="bar")
    plt.title("error_by_model_deobf")
    save_fig("by_model_deobf.png", SUBDIR, True)

    plt.figure()
    g = df.groupby("is_obfuscation")["is_error"].mean()
    g.index = ["Deobf", "Obf"]
    g.plot(kind="bar")
    plt.title("error_general_task")
    save_fig("general_task.png", SUBDIR, True)

    plt.figure()
    df.groupby("strategy")["is_error"].mean().plot(kind="bar")
    plt.title("error_by_strategy")
    save_fig("by_strategy.png", SUBDIR, True)