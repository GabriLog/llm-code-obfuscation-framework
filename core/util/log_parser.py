import re
from pathlib import Path
from typing import Optional

from core.domain.parsed_log import ParsedLog


def _extract_section(text: str, section_header: str, next_headers: list[str]) -> tuple[Optional[float], str]:
    pattern = re.escape(section_header)
    match = re.search(pattern, text)
    if not match:
        return None, ""

    section_start = match.end()

    end_pos = len(text)
    for header in next_headers:
        m = re.search(re.escape(header), text[section_start:])
        if m:
            end_pos = min(end_pos, section_start + m.start())

    section_text = text[section_start:end_pos].strip()

    time_match = re.search(r"Time:\s*([\d.]+)s", section_text)
    time_val = float(time_match.group(1)) if time_match else None

    result_match = re.search(r"Result:\s*\n(.*)", section_text, re.DOTALL)
    code = result_match.group(1).strip() if result_match else ""

    return time_val, code


def parse_log(log_path: str | Path) -> ParsedLog:
    path = Path(log_path)
    text = path.read_text(encoding="utf-8")
    parsed = ParsedLog(source_file=str(path))

    ts_match = re.search(r"Experiment Timestamp:\s*(.+)", text)
    parsed.timestamp = ts_match.group(1).strip() if ts_match else ""
    model_match = re.search(r"Model:\s*(.+)", text)
    parsed.model = model_match.group(1).strip() if model_match else ""
    strategy_match = re.search(r"Strategy:\s*(.+)", text)
    parsed.strategy = strategy_match.group(1).strip() if strategy_match else ""
    dataset_match = re.search(r"Dataset:\s*(.+)", text)
    parsed.dataset = dataset_match.group(1).strip() if dataset_match else ""
    script_match = re.search(r"Script:\s*(.+)", text)
    parsed.script_name = script_match.group(1).strip() if script_match else ""

    HEADERS = [
        "--- Obfuscation Traditional ---",
        "--- Obfuscation LLM ---",
        "--- Deobfuscation LLM ---",
    ]
    parsed.time_obf_traditional, parsed.obf_traditional = _extract_section(
        text, HEADERS[0], HEADERS[1:]
    )
    parsed.time_obf_llm, parsed.obf_llm = _extract_section(
        text, HEADERS[1], HEADERS[2:]
    )
    parsed.time_deob_llm, parsed.deob_llm = _extract_section(
        text, HEADERS[2], []
    )
    return parsed


def parse_all_logs(logs_dir: str | Path) -> list[ParsedLog]:
    logs_path = Path(logs_dir)
    log_files = sorted(logs_path.glob("*.txt"))
    return [parse_log(f) for f in log_files]
