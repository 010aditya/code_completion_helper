import os
import json
from datetime import datetime

class MetadataAgent:
    def __init__(self, log_dir="logs/manual_review"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

    def annotate(self, filename, status, notes="", tags=None):
        metadata = {
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "notes": notes,
            "tags": tags or []
        }
        log_path = os.path.join(self.log_dir, f"{os.path.basename(filename)}.json")
        with open(log_path, "w") as f:
            json.dump(metadata, f, indent=2)
        return metadata
