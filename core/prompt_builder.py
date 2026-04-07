from langchain_core.prompts import PromptTemplate
from pathlib import Path

DATASETS_PATH = Path("datasets")


def load_examples(dataset, script_name, task, max_examples=1):
    original_path = DATASETS_PATH / "original" / dataset
    obfuscation_path = DATASETS_PATH / "obfuscation" / dataset

    count = 0
    for org in original_path.glob("*.js"):
        if org.name == script_name:
            continue
        obf = obfuscation_path / org.name
        if not obf.exists():
            continue

        original_code = org.read_text(encoding="utf-8")
        obfuscated_code = obf.read_text(encoding="utf-8")
        if task == "ofuscar":
            yield original_code, obfuscated_code
        else: 
            yield obfuscated_code, original_code

        count += 1
        if count >= max_examples:
            break

def build_zeroshot(base_prompt):
    return PromptTemplate.from_template(base_prompt)

def build_fewshot(base_prompt, examples):
    examples_block = ""
    for original, transformed in examples:
        safe_original = original.replace("{", "{{").replace("}", "}}")
        safe_transformed = transformed.replace("{", "{{").replace("}", "}}")
        examples_block += (
            f"\n### EXAMPLE START ###\n"
            f"INPUT:\n{safe_original}\n"
            f"OUTPUT:\n{safe_transformed}\n"
            f"### EXAMPLE END ###\n"
        )
    final_prompt = base_prompt.replace(
        "Code:\n{code}",
        f"{examples_block}\n"
        f"Now apply the same transformation to the following code.\n"
        f"INPUT:\n{{code}}\n"
        f"OUTPUT:"
    )
    return PromptTemplate.from_template(final_prompt)
