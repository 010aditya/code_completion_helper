import os
import json

class FrameworkInjectionAgent:
    def __init__(self, migrated_dir, mapping_file="config/framework_mapping.json"):
        self.migrated_dir = migrated_dir
        self.mapping_file = mapping_file
        with open(self.mapping_file, "r") as f:
            self.framework_map = json.load(f)

    def inject_framework_references(self):
        modified_files = []
        for root, _, files in os.walk(self.migrated_dir):
            for file in files:
                if file.endswith(".java"):
                    path = os.path.join(root, file)
                    with open(path, "r") as f:
                        code = f.read()
                    updated_code = self._rewrite_framework_refs(code)
                    if updated_code != code:
                        with open(path, "w") as f:
                            f.write(updated_code)
                        modified_files.append(path)
        return modified_files

    def _rewrite_framework_refs(self, code):
        for legacy_ref, modern_ref in self.framework_map.items():
            code = code.replace(legacy_ref, modern_ref)
        return code
