import json
from pathlib import Path

def load_config():
    cfg_path = Path("data/config.json")
    if not cfg_path.exists():
        raise FileNotFoundError("data/config.json not found")
    with cfg_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if "steam32_id" not in data:
        raise KeyError("config missing 'steam32_id'")
    return data
