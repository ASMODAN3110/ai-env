from datetime import datetime
import json

class Log:
    def __init__(self, level, message, module, context=None, timestamp=None, id=None):
        self.id = id
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.level = level.upper()
        self.message = message
        self.module = module
        self.context = context or {}

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "level": self.level,
            "message": self.message,
            "module": self.module,
            "context": json.dumps(self.context)
        }

    def __repr__(self):
        return f"[{self.timestamp}] {self.level} | {self.module} | {self.message} | context: {self.context}"
