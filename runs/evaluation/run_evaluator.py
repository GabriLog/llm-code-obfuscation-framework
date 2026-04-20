from pathlib import Path
from typing import Optional

from core.domain.eval_result import EvalResult
from core.util.js_utils import compute_ast_similarity, run_js_code

AST_SCRIPT = Path(__file__).parent / "ast_similarity.js"
TIMEOUT_SECONDS = 10


def evaluate_pair(
    label: str,
    original_code: str,
    result_code: str,
    time_seconds: Optional[float] = None,
) -> EvalResult:
    
    result = EvalResult(label=label, time_seconds=time_seconds)

    ast_data = compute_ast_similarity(original_code, result_code)
    result.ast_score = ast_data.get("score")
    result.ast_nodes_original = ast_data.get("nodes_a", 0)
    result.ast_nodes_result = ast_data.get("nodes_b", 0)
    result.ast_parse_error = ast_data.get("parse_error") or ast_data.get("error")

    out_original, err_orig = run_js_code(original_code)
    out_result, err_result = run_js_code(result_code)
    result.output_original = out_original
    result.output_result = out_result
    result.execution_error = err_result
    result.functional_match = (
        err_result is None and out_original == out_result
    )
    return result


def evaluate_experiment(
    original_code: str,
    obf_traditional: str,
    obf_llm: str,
    deob_llm: str,
    time_obf_traditional: Optional[float] = None,
    time_obf_llm: Optional[float] = None,
    time_deob_llm: Optional[float] = None,
) -> list[EvalResult]:
    
    results = []
    
    results.append(evaluate_pair(
        label="obf_tradicional",
        original_code=original_code,
        result_code=obf_traditional,
        time_seconds=time_obf_traditional,
    ))
    results.append(evaluate_pair(
        label="obf_llm",
        original_code=original_code,
        result_code=obf_llm,
        time_seconds=time_obf_llm,
    ))
    results.append(evaluate_pair(
        label="deob_llm",
        original_code=original_code,
        result_code=deob_llm,
        time_seconds=time_deob_llm,
    ))
    return results
