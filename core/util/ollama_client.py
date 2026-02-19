import subprocess


def list_models():
    result = subprocess.run(
        ["ollama", "list"], 
        capture_output=True, 
        text=True
    )
    lines = result.stdout.strip().split("\n")[1:]
    return [line.split()[0] for line in lines]
