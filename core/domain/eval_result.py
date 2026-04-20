from dataclasses import dataclass
from typing import Optional

@dataclass
class EvalResult:
    label: str
    ast_score: Optional[float] = None
    ast_nodes_original: int = 0
    ast_nodes_result: int = 0
    ast_parse_error: Optional[str] = None
    functional_match: Optional[bool] = None
    output_original: str = ""
    output_result: str = ""
    execution_error: Optional[str] = None
    time_seconds: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "ast_score": self.ast_score,
            "ast_nodes_original": self.ast_nodes_original,
            "ast_nodes_result": self.ast_nodes_result,
            "ast_parse_error": self.ast_parse_error,
            "functional_match": self.functional_match,
            "output_original": self.output_original,
            "output_result": self.output_result,
            "execution_error": self.execution_error,
            "time_seconds": self.time_seconds,
        }