import os
import subprocess

class BuildValidatorAgent:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def validate(self):
        results = {}
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    try:
                        subprocess.run(
                            ["javac", file_path],
                            check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        results[file] = True
                    except subprocess.CalledProcessError as e:
                        print(f"[BuildValidatorAgent] Compilation failed for {file}: {e.stderr.decode()}")
                        results[file] = False
        return results
