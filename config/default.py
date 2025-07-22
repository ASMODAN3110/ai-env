from pathlib import Path

from config import AIProjectConfig

config = AIProjectConfig()

config.model.epochs = 200

config.to_json(Path("config.json"))
