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
    files = [f for f in OUTPUT_DIR.rglob("*.json") if f.name != "chart_summary.json"]
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


def build_summary(df, df_obf, df_deob):

    def safe(val):
        if val is None:
            return None
        try:
            import math
            if math.isnan(val):
                return None
        except TypeError:
            pass
        return round(float(val), 4)

    summary = {}
    df_llm  = df_obf[df_obf["label"] == "obf_llm"] 
    df_trad = df_obf[df_obf["label"] == "obf_tradicional"]

    summary["ast_overview"] = {
        model: {
            "ast_score_obf":  safe(df_llm.groupby("model")["ast_score"].mean().get(model)),  # 👈
            "ast_score_deob": safe(df_deob.groupby("model")["ast_score"].mean().get(model)),
            "node_ratio_obf": safe(df_llm.groupby("model")["node_ratio"].mean().get(model)), # 👈
        }
        for model in sorted(df["model"].dropna().unique())
    }

    summary["error_and_functional"] = {
        model: {
            lbl: {
                "error_rate":      safe(df[df["label"] == lbl].groupby("model")["is_error"].mean().get(model)),
                "functional_match": safe(df[df["label"] == lbl].groupby("model")["functional_match"].mean().get(model)),
            }
            for lbl in ["obf_llm", "deob_llm"]
        }
        for model in sorted(df["model"].dropna().unique())
    }

    df_trad = df[df["label"] == "obf_tradicional"]
    summary["error_and_functional"]["obf_tradicional_global"] = {
        "error_rate":       safe(df_trad["is_error"].mean()),
        "functional_match": safe(df_trad["functional_match"].mean()),
    }
    summary["strategy_impact"] = {}
    for strategy in df["strategy"].dropna().unique():
        sub = df[df["strategy"] == strategy]
        summary["strategy_impact"][strategy] = {
            lbl: {
                "functional_match": safe(sub[sub["label"] == lbl]["functional_match"].mean()),
                "error_rate":       safe(sub[sub["label"] == lbl]["is_error"].mean()),
            }
            for lbl in sub["label"].dropna().unique()
        }

    df_llm  = df_obf[df_obf["label"] == "obf_llm"]
    summary["quality_overview"] = {
        model: {
            "ast_score_obf_llm":        safe(df_llm[df_llm["functional_match"] == True].groupby("model")["ast_score"].mean().get(model)),
            "node_ratio_obf_llm":       safe(df_llm.groupby("model")["node_ratio"].mean().get(model)),
            "functional_match_obf_llm": safe(df_llm.groupby("model")["functional_match"].mean().get(model)),
        }
        for model in sorted(df_llm["model"].dropna().unique())
    }
    summary["quality_overview"]["obf_tradicional"] = {
        "ast_score":        safe(df_trad["ast_score"].mean()),
        "node_ratio":       safe(df_trad["node_ratio"].mean()),
        "functional_match": safe(df_trad["functional_match"].mean()),
    }
    summary["time_overview"] = {
        model: {
            lbl: safe(df[df["label"] == lbl].groupby("model")["time_seconds"].mean().get(model))
            for lbl in ["obf_tradicional", "obf_llm", "deob_llm"]
        }
        for model in sorted(df["model"].dropna().unique())
    }
    return summary


def main():
    df = load_data()

    df["is_obfuscation"]   = df["label"].str.contains("obf", na=False)
    df["is_deobfuscation"] = df["label"].str.contains("deob", na=False)
    df["is_error"]         = df["execution_error"].notna()
    df["node_ratio"]       = df["ast_nodes_result"] / df["ast_nodes_original"]
    df.loc[df["ast_nodes_original"] == 0, "node_ratio"] = None

    df_obf  = df[df["label"].isin(["obf_tradicional", "obf_llm"])]
    df_deob = df[df["label"] == "deob_llm"]

    plot_functional(df, df_obf, df_deob)
    plot_error(df, df_obf, df_deob)
    plot_time(df, df_obf)
    plot_ast(df, df_obf, df_deob)
    plot_quality(df, df_obf)

    summary = build_summary(df, df_obf, df_deob)
    summary_path = OUTPUT_DIR / "chart_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("✔ Todas las gráficas generadas correctamente")
    print(f"✔ Resumen guardado en {summary_path}")


if __name__ == "__main__":
    main()