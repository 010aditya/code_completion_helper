import os
import json
from openai import OpenAI
from agents.context_stitcher import ContextStitcherAgent

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FixAndCompileAgent:
    def __init__(self, legacy_dir, migrated_dir):
        self.legacy_dir = legacy_dir
        self.migrated_dir = migrated_dir

    def fix_file(self, target_path, stitcher: ContextStitcherAgent):
        assert self.legacy_dir not in target_path, "❌ Attempted to write to legacy directory. Aborting."

        migrated_file_path = os.path.join(self.migrated_dir, target_path)

        if not os.path.exists(migrated_file_path):
            print(f"❌ File not found: {migrated_file_path}")
            return {"fix_log": {"file_missing": True}, "fixed_code": ""}

        # Step 1: Read migrated code
        with open(migrated_file_path, "r", encoding="utf-8") as f:
            original_code = f.read()

        # Step 2: Get legacy context
        legacy_context = stitcher.get_context_for_file(target_path)

        # Step 3: GPT Prompt
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert Java migration assistant. Fix compilation issues in migrated code "
                    "using the legacy context and ensure clean, idiomatic Spring Boot architecture."
                )
            },
            {
                "role": "user",
                "content": f"""
Legacy context (from original Java class or related files):
```
{legacy_context}
```

Broken migrated code:
```
{original_code}
```

Please:
1. Fix all compilation issues
2. Add missing method stubs if needed
3. Ensure all injections (`@Autowired`, etc.) are present
4. Return:
```json
{{
  "missing_method": true,
  "injection_resolved": true,
  "field_type_fix": false,
  "generated_stub": true
}}
```
Then provide the fixed Java code.
"""
            }
        ]

        # Step 4: Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.2
        )

        output = response.choices[0].message.content.strip()

        # Step 5: Parse GPT response
        fix_log = {}
        fixed_code = ""

        try:
            if output.startswith("{") and "missing_method" in output:
                json_part, rest = output.split("```", 1)
                fix_log = json.loads(json_part)
                fixed_code = rest.split("```")[-2].strip()
            else:
                fixed_code = output
                fix_log = {"gpt_format_unstructured": True}
        except Exception as e:
            print("⚠️ Failed to parse structured GPT fix output. Defaulting to raw code.")
            fixed_code = output
            fix_log = {"gpt_parse_error": True}

        # Step 6: Compare and log
        if original_code.strip() == fixed_code.strip():
            fix_log["gpt_no_change"] = True

        # Step 7: Save fixed code
        with open(migrated_file_path, "w", encoding="utf-8") as f:
            f.write(fixed_code)

        print(f"✅ Fixed {target_path}")
        return {"fix_log": fix_log, "fixed_code": fixed_code}
