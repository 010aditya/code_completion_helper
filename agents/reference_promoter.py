import os
import shutil
import json

class ReferencePromoterAgent:
    def __init__(self, fix_history_dir="logs/fix_history", reference_dir="reference_apps/promoted"):
        self.fix_history_dir = fix_history_dir
        self.reference_dir = reference_dir
        os.makedirs(reference_dir, exist_ok=True)

    def promote_successful_fixes(self):
        for file in os.listdir(self.fix_history_dir):
            if file.endswith(".json"):
                path = os.path.join(self.fix_history_dir, file)
                with open(path, "r") as f:
                    entry = json.load(f)
                if entry.get("success") and entry.get("original") != entry.get("fixed"):
                    base = file.replace(".json", "")
                    legacy_file = os.path.join(self.reference_dir, base + "_legacy.java")
                    migrated_file = os.path.join(self.reference_dir, base + "_migrated.java")
                    with open(legacy_file, "w") as lf:
                        lf.write(entry["original"])
                    with open(migrated_file, "w") as mf:
                        mf.write(entry["fixed"])
