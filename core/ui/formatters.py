from typing import Optional


def format_score(score: Optional[float]) -> str:
    if score is None:
        return "[red]ERR[/red]"
    color = "green" if score >= 0.8 else "yellow" if score >= 0.5 else "red"
    return f"[{color}]{score:.3f}[/{color}]"

def format_match(match: Optional[bool]) -> str:
    if match is None:
        return "[red]ERR[/red]"
    return "[green]✓ PASS[/green]" if match else "[red]✗ FAIL[/red]"

def format_time(t: Optional[float]) -> str:
    if t is None:
        return "—"
    return f"{t:.2f}s"