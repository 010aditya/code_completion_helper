import os
import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer, util

class FrameworkMappingSuggesterAgent:
    def __init__(self, legacy_dir, springboot_dir, output_path="config/suggested_framework_mapping.json"):
        self.legacy_dir = legacy_dir
        self.springboot_dir = springboot_dir
        self.output_path = output_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def suggest_mappings(self, top_k=1):
        legacy_classes = self._extract_class_summaries(self.legacy_dir)
        spring_classes = self._extract_class_summaries(self.springboot_dir)

        legacy_keys = list(legacy_classes.keys())
        legacy_embeds = self.model.encode(list(legacy_classes.values()), convert_to_tensor=True)
        spring_keys = list(spring_classes.keys())
        spring_embeds = self.model.encode(list(spring_classes.values()), convert_to_tensor=True)

        suggestions = {}
        scores = util.cos_sim(legacy_embeds, spring_embeds)

        for i, legacy_fqn in enumerate(legacy_keys):
            top_matches = torch.topk(scores[i], k=top_k)
            top_idx = top_matches.indices[0].item()
            top_score = top_matches.values[0].item()
            if top_score > 0.6:
                spring_fqn = spring_keys[top_idx]
                suggestions[legacy_fqn] = spring_fqn

        with open(self.output_path, "w") as f:
            json.dump(suggestions, f, indent=2)

        return suggestions

    def _extract_class_summaries(self, base_dir):
        summaries = {}
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".java"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read()
                        fqn = self._get_fully_qualified_name(path, content, base_dir)
                        summary = self._summarize_class(content)
                        if fqn and summary:
                            summaries[fqn] = summary
                    except:
                        continue
        return summaries

    def _get_fully_qualified_name(self, file_path, content, base_dir):
        m = re.search(r'package\s+([\w.]+);', content)
        cls = re.search(r'(public\s+)?(class|interface|enum)\s+(\w+)', content)
        if m and cls:
            return f"{m.group(1)}.{cls.group(3)}"
        rel_path = os.path.relpath(file_path, base_dir).replace(os.sep, ".").replace(".java", "")
        return rel_path

    def _summarize_class(self, content):
        lines = content.splitlines()
        method_signatures = []
        for line in lines:
            line = line.strip()
            if line.startswith("public") and ("(" in line and ")" in line):
                method_signatures.append(line)
        return " ".join(method_signatures[:10])  # trim to avoid long tokens
