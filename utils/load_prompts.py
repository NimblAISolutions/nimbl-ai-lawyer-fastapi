from pathlib import Path

def get_prompts(path: str | Path = "prompts.json"):
    from json import load
    with open(path, "r") as f:
        return load(f)