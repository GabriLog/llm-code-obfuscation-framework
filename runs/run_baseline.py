import subprocess

def run_baseline(experiment):
    cmd = [
        "node",
        "runs/obfuscator.js",
        experiment.dataset,
        experiment.script_name,
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True
    )
    return float(result.stdout.strip())
