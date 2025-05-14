import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class EmbeddingIndexerAgent:
    def __init__(self, reference_dir, index_path="data/embedding_index.json"):
        self.reference_dir = reference_dir
        self.index_path = index_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = []

    def index_all(self):
        for root, _, files in os.walk(self.reference_dir):
            for file in files:
                if file.endswith("_legacy.java"):
                    legacy_path = os.path.join(root, file)
                    migrated_path = legacy_path.replace("_legacy.java", "_migrated.java")
                    if os.path.exists(migrated_path):
                        with open(legacy_path, "r") as lf, open(migrated_path, "r") as mf:
                            legacy_code = lf.read()
                            migrated_code = mf.read()
                        embedding = self.model.encode(legacy_code)
                        self.index.append({
                            "legacy_path": legacy_path,
                            "migrated_path": migrated_path,
                            "embedding": embedding.tolist()
                        })
        with open(self.index_path, "w") as f:
            json.dump(self.index, f, indent=2)
