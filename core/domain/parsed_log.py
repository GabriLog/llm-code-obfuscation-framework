from dataclasses import dataclass
from typing import Optional

@dataclass
class ParsedLog:
    timestamp: str = ""
    model: str = ""
    strategy: str = ""
    dataset: str = ""
    script_name: str = ""
    time_obf_traditional: Optional[float] = None
    time_obf_llm: Optional[float] = None
    time_deob_llm: Optional[float] = None
    obf_traditional: str = ""
    obf_llm: str = ""
    deob_llm: str = ""
    source_file: str = ""