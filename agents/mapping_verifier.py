import json
import os

class MappingVerifierAgent:
    def __init__(self, mapping_file):
        self.mapping_file = mapping_file
        self.mappings = []

    def verify(self):
        if not os.path.exists(self.mapping_file):
            raise FileNotFoundError(f"Mapping file not found: {self.mapping_file}")

        with open(self.mapping_file, "r") as f:
            try:
                self.mappings = json.load(f)
                if not isinstance(self.mappings, list):
                    raise ValueError("Expected mapping.json to be a list of mappings.")
                for m in self.mappings:
                    if "sourcePath" not in m or "targetPath" not in m:
                        raise ValueError("Each mapping must contain sourcePath and targetPath.")
            except Exception as e:
                raise ValueError(f"Invalid mapping file: {e}")

        print(f"[MappingVerifierAgent] ✅ Loaded {len(self.mappings)} mappings.")
        return self.mappings
