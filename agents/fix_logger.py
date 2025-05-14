import os
import json
from datetime import datetime

class FixHistoryLogger:
    def __init__(self, log_dir="logs/fix_history"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def log_fix(self, filename, original, fixed, success=True):
        log_entry = {
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "original": original,
            "fixed": fixed
        }
        log_path = os.path.join(self.log_dir, f"{os.path.basename(filename)}.json")
        with open(log_path, "w") as f:
            json.dump(log_entry, f, indent=2)
