import os
import openai

class CompletionAgent:
    def __init__(self, legacy_dir, api_key=None):
        self.legacy_dir = legacy_dir
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def suggest_completion(self, missing_method_name, context_class):
        legacy_code = self._find_class_code(context_class)
        if not legacy_code:
            return None

        prompt = f"""
Given the following legacy class and a missing method named '{missing_method_name}', 
please suggest the most likely method implementation that could be migrated to the new codebase.

LEGACY CLASS:
{legacy_code}

Only return a compilable Java method that likely implements {missing_method_name}.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[CompletionAgent] Error: {e}")
            return None

    def _find_class_code(self, class_name):
        for root, _, files in os.walk(self.legacy_dir):
            for file in files:
                if file.endswith(".java") and class_name in file:
                    try:
                        with open(os.path.join(root, file), "r") as f:
                            return f.read()
                    except:
                        continue
        return None
