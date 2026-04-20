import subprocess
import tempfile
import os
import re
import json
from pathlib import Path

AST_SCRIPT = Path(__file__).parent.parent.parent / "runs" / "evaluation" / "ast_similarity.js"
TIMEOUT_SECONDS = 10


def _write_temp_js(code: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".js")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(code)
    return path


def _extract_error_message(stderr: str) -> str:
    if not stderr:
        return ""
    
    for line in stderr.splitlines():
        line = line.strip()
        if re.match(r'^(SyntaxError|TypeError|ReferenceError|RangeError|Error):', line):
            return line
        
    for line in stderr.splitlines():
        line = line.strip()
        if line and not line.startswith("at ") and not line.startswith("Node.js"):
            return line
        
    return stderr.splitlines()[0].strip()


def compute_ast_similarity(original_code: str, result_code: str) -> dict:
    path_a = _write_temp_js(original_code)
    path_b = _write_temp_js(result_code)
    try:
        proc = subprocess.run(
            ["node", str(AST_SCRIPT), path_a, path_b],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        if proc.returncode != 0:
            print("NODE ERROR:", proc.stderr)
            return {"score": None, "error": proc.stderr.strip()}
        return json.loads(proc.stdout.strip())
    
    except subprocess.TimeoutExpired:
        return {"score": None, "error": "timeout"}
    
    except Exception as e:
        return {"score": None, "error": str(e)}
    
    finally:
        os.unlink(path_a)
        os.unlink(path_b)


def run_js_code(code: str) -> tuple[str, str | None]:
    path = _write_temp_js(code)
    try:
        proc = subprocess.run(
            ["node", path],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        stdout = proc.stdout.strip()
        stderr = _extract_error_message(proc.stderr) if proc.returncode != 0 else None
        return stdout, stderr
    
    except subprocess.TimeoutExpired:
        return "", "timeout"
    
    except Exception as e:
        return "", str(e)
    
    finally:
        os.unlink(path)