import json
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_data():
    files = list(OUTPUT_DIR.rglob("*.json"))
    all_data = []

    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)

        for run in data:
            for r in run.get("results", []):
                all_data.append({
                "timestamp": run.get("timestamp"),
                "model": run.get("model"),
                "strategy": run.get("strategy"),
                "dataset": run.get("dataset"),
                "script": run.get("script"),
                "label": r.get("label"),

                "ast_score": r.get("ast_score"),
                "ast_nodes_original": r.get("ast_nodes_original"),
                "ast_nodes_result": r.get("ast_nodes_result"),

                "functional_match": r.get("functional_match"),
                "time_seconds": r.get("time_seconds"),

                "execution_error": r.get("execution_error"),
                "ast_parse_error": r.get("ast_parse_error"),
            })
    return pd.DataFrame(all_data)

df = load_data()

df["is_obfuscation"] = df["label"].str.contains("obf", na=False)
df["is_deobfuscation"] = df["label"].str.contains("deob", na=False)
df["is_error"] = df["execution_error"].notna()

def save_fig(name, force_unit=False):
    if force_unit:
        plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / name, dpi=300)
    plt.close()


#1
plt.figure()
df.groupby("model")["functional_match"].mean().plot(kind="bar")
plt.title("functional_by_model (ALL)")
plt.ylabel("rate")
save_fig("functional_by_model_all.png", force_unit=True)

plt.figure()
df[df["is_obfuscation"]].groupby("model")["functional_match"].mean().plot(kind="bar")
plt.title("functional_by_model (OBF)")
plt.ylabel("rate")
save_fig("functional_by_model_obf.png", force_unit=True)

plt.figure()
df[df["is_deobfuscation"]].groupby("model")["functional_match"].mean().plot(kind="bar")
plt.title("functional_by_model (DEOBF)")
plt.ylabel("rate")
save_fig("functional_by_model_deobf.png", force_unit=True)

plt.figure()
g = df.groupby("is_obfuscation")["functional_match"].mean()
g.index = ["Deobfuscation" if not x else "Obfuscation" for x in g.index]
g.plot(kind="bar")
plt.title("functional_general_task (OBF vs DEOBF)")
plt.ylabel("rate")
save_fig("functional_general_task.png", force_unit=True)

plt.figure()
g = df.groupby("strategy")["functional_match"].mean()
g.plot(kind="bar")
plt.title("functional_general_strategy (zero vs few-shot)")
plt.ylabel("rate")
save_fig("functional_general_strategy.png", force_unit=True)


#2
plt.figure()
df.groupby("model")["is_error"].mean().plot(kind="bar")
plt.title("error_rate_by_model (ALL)")
plt.ylabel("rate")
save_fig("error_rate_by_model_all.png", force_unit=True)

plt.figure()
df[df["is_obfuscation"]].groupby("model")["is_error"].mean().plot(kind="bar")
plt.title("error_rate_by_model (OBF)")
plt.ylabel("rate")
save_fig("error_rate_by_model_obf.png", force_unit=True)

plt.figure()
df[df["is_deobfuscation"]].groupby("model")["is_error"].mean().plot(kind="bar")
plt.title("error_rate_by_model (DEOBF)")
plt.ylabel("rate")
save_fig("error_rate_by_model_deobf.png", force_unit=True)

plt.figure()
g = df.groupby("is_obfuscation")["is_error"].mean()
g.index = ["Deobfuscation" if not x else "Obfuscation" for x in g.index]
g.plot(kind="bar")
plt.title("error_rate_general_task (OBF vs DEOBF)")
plt.ylabel("rate")
save_fig("error_rate_general_task.png", force_unit=True)

plt.figure()
g = df.groupby("strategy")["is_error"].mean()
g.plot(kind="bar")
plt.title("error_rate_general_strategy (zero vs few-shot)")
plt.ylabel("rate")
save_fig("error_rate_general_strategy.png", force_unit=True)


#3
plt.figure()
df.groupby("model")["time_seconds"].mean().plot(kind="bar")
plt.title("avg_time_by_model (ALL)")
plt.ylabel("seconds")
save_fig("avg_time_by_model_all.png")

plt.figure()
df[df["is_obfuscation"]].groupby("model")["time_seconds"].mean().plot(kind="bar")
plt.title("avg_time_by_model (OBF)")
plt.ylabel("seconds")
save_fig("avg_time_by_model_obf.png")

plt.figure()
df[df["is_deobfuscation"]].groupby("model")["time_seconds"].mean().plot(kind="bar")
plt.title("avg_time_by_model (DEOBF)")
plt.ylabel("seconds")
save_fig("avg_time_by_model_deobf.png")

plt.figure()
g = df.groupby("is_obfuscation")["time_seconds"].mean()
g.index = ["Deobfuscation" if not x else "Obfuscation" for x in g.index]
g.plot(kind="bar")
plt.title("avg_time_general_task (OBF vs DEOBF)")
plt.ylabel("seconds")
save_fig("avg_time_general_task.png")

plt.figure()
g = df.groupby("strategy")["time_seconds"].mean()
g.plot(kind="bar")
plt.title("avg_time_general_strategy (zero vs few-shot)")
plt.ylabel("seconds")
save_fig("avg_time_general_strategy.png")

""" Falta
· tiempo LLM vs trad (ratio)
· scatter tiempo vs ast_score
· tiempo por dataset (small/large)
"""


#4
plt.figure()
df[df["is_obfuscation"]].groupby("model")["ast_score"].mean().plot(kind="bar")
plt.title("ast_by_model (OBF)")
plt.ylabel("score")
save_fig("ast_by_model_obf.png")

plt.figure()
df[(df["is_obfuscation"]) & (df["strategy"] == "zero-shot")] \
    .groupby("model")["ast_score"].mean().plot(kind="bar")
plt.title("ast_by_model (OBF ZERO-SHOT)")
plt.ylabel("score")
save_fig("ast_by_model_obf_zero_shot.png")

plt.figure()
df[(df["is_obfuscation"]) & (df["strategy"] == "few-shot")] \
    .groupby("model")["ast_score"].mean().plot(kind="bar")
plt.title("ast_by_model (OBF FEW-SHOT)")
plt.ylabel("score")
save_fig("ast_by_model_obf_few_shot.png")

plt.figure()
g = df[df["is_obfuscation"]].groupby("strategy")["ast_score"].mean()
g.plot(kind="bar")
plt.title("ast_general_strategy_obf (zero vs few-shot)")
plt.ylabel("score")
save_fig("ast_general_strategy_obf.png")

plt.figure()
df[df["is_deobfuscation"]].groupby("model")["ast_score"].mean().plot(kind="bar")
plt.title("ast_by_model (DEOBF)")
plt.ylabel("score")
save_fig("ast_by_model_deobf.png")

plt.figure()
df[(df["is_deobfuscation"]) & (df["strategy"] == "zero-shot")] \
    .groupby("model")["ast_score"].mean().plot(kind="bar")
plt.title("ast_by_model (DEOBF ZERO-SHOT)")
plt.ylabel("score")
save_fig("ast_by_model_deobf_zero_shot.png")

plt.figure()
df[(df["is_deobfuscation"]) & (df["strategy"] == "few-shot")] \
    .groupby("model")["ast_score"].mean().plot(kind="bar")
plt.title("ast_by_model (DEOBF FEW-SHOT)")
plt.ylabel("score")
save_fig("ast_by_model_deobf_few_shot.png")

plt.figure()
g = df[df["is_deobfuscation"]].groupby("strategy")["ast_score"].mean()
g.plot(kind="bar")
plt.title("ast_general_strategy_deobf (zero vs few-shot)")
plt.ylabel("score")
save_fig("ast_general_strategy_deobf.png")


#5
""" Falta
· ast_score solo en casos functional=true
· node_ratio (nodos_result/nodos_orig)
· scatter ast_score vs node_ratio
· trad vs LLM: tiempo + functional
"""





"""
1. functional.py -> Tasa de éxito
2. error.py -> Tasa de errores
3. time.py -> Tiempos de ejecución
4. ast.py -> Similitud AST
5. quality.py -> Calidad cruzada
"""


print("✔ Todas las gráficas generadas correctamente en /outputs")