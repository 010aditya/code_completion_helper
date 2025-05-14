import os
import openai
from agents.fix_logger import FixHistoryLogger
from agents.context_stitcher import ContextStitcherAgent

class FixAndCompileAgent:
    def __init__(self, legacy_dir, migrated_dir, api_key=None):
        self.legacy_dir = legacy_dir
        self.migrated_dir = migrated_dir
        self.fix_logger = FixHistoryLogger()
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def fix_file(self, filename, context_stitcher: ContextStitcherAgent):
        file_path = os.path.join(self.migrated_dir, filename)
        legacy_context = context_stitcher.get_stitched_context(filename)

        try:
            with open(file_path, "r") as f:
                migrated_code = f.read()
        except Exception as e:
            print(f"[FixAndCompileAgent] Error reading {filename}: {e}")
            return False

        prompt = f"""
You are an expert Java developer. Given the migrated but broken Java class below,
fix it to be fully functional and compilable. Use the legacy context provided to
restore missing methods and references.

LEGACY CONTEXT:
{legacy_context}

MIGRATED CODE TO FIX:
{migrated_code}

RETURN ONLY VALID JAVA CODE.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=3000
            )
            fixed_code = response.choices[0].message.content.strip()
            with open(file_path, "w") as f:
                f.write(fixed_code)
            self.fix_logger.log_fix(filename, migrated_code, fixed_code, success=True)
            print(f"[FixAndCompileAgent] Fixed {filename}")
            return True

        except Exception as e:
            print(f"[FixAndCompileAgent] GPT fix failed for {filename}: {e}")
            self.fix_logger.log_fix(filename, migrated_code, migrated_code, success=False)
            return False
