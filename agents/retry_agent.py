import os
import json
from agents.fix_and_compile import FixAndCompileAgent
from agents.context_stitcher import ContextStitcherAgent

class RetryAgent:
    def __init__(self, fix_dir="logs/fix_history", legacy_dir=None, migrated_dir=None):
        self.fix_dir = fix_dir
        self.legacy_dir = legacy_dir
        self.migrated_dir = migrated_dir

    def retry_all_failures(self, api_key=None):
        context_stitcher = ContextStitcherAgent(self.legacy_dir)
        fixer = FixAndCompileAgent(self.legacy_dir, self.migrated_dir, api_key)

        for file in os.listdir(self.fix_dir):
            if file.endswith(".json"):
                path = os.path.join(self.fix_dir, file)
                with open(path, "r") as f:
                    entry = json.load(f)
                if not entry.get("success"):
                    java_file = entry["filename"]
                    print(f"[RetryAgent] Retrying {java_file}...")
                    fixer.fix_file(java_file, context_stitcher)
