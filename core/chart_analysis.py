import json
import pandas as pd
from pathlib import Path

from charts.functional import plot_functional
from charts.error import plot_error
from charts.time import plot_time
from charts.ast import plot_ast
from charts.quality import plot_quality

OUTPUT_DIR = Path("outputs")


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


def main():

    df = load_data()

    df["is_obfuscation"] = df["label"].str.contains("obf", na=False)
    df["is_deobfuscation"] = df["label"].str.contains("deob", na=False)
    df["is_error"] = df["execution_error"].notna()
    
    df["node_ratio"] = df["ast_nodes_result"] / df["ast_nodes_original"]
    df.loc[df["ast_nodes_original"] == 0, "node_ratio"] = None

    df_obf = df[df["label"].isin(["obf_tradicional", "obf_llm"])]
    df_deob = df[df["label"] == "deob_llm"]
    df_valid_ast = df[df["ast_score"] > 0]

    plot_functional(df, df_obf, df_deob)
    plot_error(df, df_obf, df_deob)
    plot_time(df, df_obf)
    plot_ast(df, df_obf, df_deob)
    plot_quality(df, df_obf)

    print("✔ Todas las gráficas generadas correctamente")


if __name__ == "__main__":
    main()