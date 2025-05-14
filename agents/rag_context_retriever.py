import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class RAGContextRetrieverAgent:
    def __init__(self, embedding_index_path="data/embedding_index.json"):
        self.embedding_index_path = embedding_index_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        with open(self.embedding_index_path, "r") as f:
            self.index = json.load(f)

    def retrieve_similar_contexts(self, legacy_snippet, top_k=3):
        query_embedding = self.model.encode(legacy_snippet).reshape(1, -1)
        embeddings = np.array([np.array(item["embedding"]) for item in self.index])
        scores = cosine_similarity(query_embedding, embeddings)[0]
        ranked = sorted(zip(scores, self.index), key=lambda x: x[0], reverse=True)
        top_matches = []

        for score, item in ranked[:top_k]:
            with open(item["migrated_path"], "r") as f:
                migrated_code = f.read()
            top_matches.append({
                "path": item["migrated_path"],
                "score": float(score),
                "code": migrated_code
            })

        return top_matches
