import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config.json"

config = json.loads(Path(CONFIG_FILE).read_text())
