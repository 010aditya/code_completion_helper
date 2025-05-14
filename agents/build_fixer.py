import os
import subprocess
import re
import json

from agents.fix_and_compile import FixAndCompileAgent
from agents.context_stitcher import ContextStitcherAgent

class BuildFixerAgent:
    def __init__(self, legacy_dir, migrated_dir, report_path="data/migration_report.json"):
        self.legacy_dir = legacy_dir
        self.migrated_dir = migrated_dir
        self.gradle_file = os.path.join(migrated_dir, "build.gradle")
        self.report_path = os.path.join(migrated_dir, report_path)
        self.max_retries = 3

    def run(self):
        for attempt in range(1, self.max_retries + 1):
            print(f"🔁 Attempt {attempt}: Running Gradle build...")

            result = subprocess.run(
                ["./gradlew", "build", "--stacktrace"],
                cwd=self.migrated_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                print("✅ Gradle build successful.")
                return True

            print("❌ Build failed. Attempting fix...")
            build_errors = result.stderr
            fixed = self.attempt_fix(build_errors)

            if not fixed:
                print("⚠️ Gradle issue could not be auto-fixed. Analyzing source-level errors...")
                broken_files = self.extract_failing_files(build_errors)

                if broken_files:
                    fixer = FixAndCompileAgent(self.legacy_dir, self.migrated_dir)
                    stitcher = ContextStitcherAgent(self.legacy_dir)

                    for file in broken_files:
                        print(f"🛠 Attempting GPT fix for: {file}")
                        try:
                            fix_result = fixer.fix_file(file, stitcher)
                            self.update_report(file, build_fixer=True, gpt_fix=True,
                                fix_status="succeeded",
                                fix_log=fix_result.get("fix_log", {})
                            )
                        except Exception as e:
                            print(f"❌ Fix failed for {file}: {e}")
                            self.update_report(file, build_fixer=True, gpt_fix=True,
                                fix_status="failed",
                                fix_log={"gpt_failed": True}
                            )
                return False
        return False

    def attempt_fix(self, log_output):
        fixed = False

        missing_dep = re.search(r"Could not find ([\w\.\-]+):([\w\.\-]+):([\w\.\-]+)", log_output)
        if missing_dep:
            group, artifact, version = missing_dep.groups()
            dep_line = f"implementation '{group}:{artifact}:{version}'"
            self._append_dependency(dep_line)
            print(f"🔧 Added missing dependency: {dep_line}")
            fixed = True

        if "invalid source release" in log_output or "error: release version" in log_output:
            self._replace_in_file("sourceCompatibility = '.*?'", "sourceCompatibility = '21'")
            print("🔧 Adjusted sourceCompatibility to Java 21.")
            fixed = True

        if "Plugin [id: 'org.springframework.boot'] was not found" in log_output:
            self._ensure_plugin("id 'org.springframework.boot' version '3.2.2'")
            print("🔧 Injected Spring Boot plugin.")
            fixed = True

        return fixed

    def extract_failing_files(self, log_output):
        return list(set(re.findall(r"(src/main/java/.*?\.java):", log_output)))

    def _append_dependency(self, line):
        with open(self.gradle_file, "a") as f:
            f.write(f"\n    {line}\n")

    def _replace_in_file(self, pattern, replacement):
        with open(self.gradle_file, "r") as f:
            content = f.read()
        content = re.sub(pattern, replacement, content)
        with open(self.gradle_file, "w") as f:
            f.write(content)

    def _ensure_plugin(self, plugin_line):
        with open(self.gradle_file, "r") as f:
            lines = f.readlines()

        if not any("org.springframework.boot" in line for line in lines):
            lines.insert(1, f"{plugin_line}\n")

        with open(self.gradle_file, "w") as f:
            f.writelines(lines)

    def update_report(self, filepath, build_fixer=False, gpt_fix=False, fix_status="not_required", fix_log=None):
        if not os.path.exists(self.report_path):
            return

        with open(self.report_path, "r") as f:
            data = json.load(f)

        updated = False
        for entry in data.get("report", []):
            if filepath in entry.get("target_path", "") or filepath in entry.get("filename", ""):
                entry["build_fixer_attempted"] = build_fixer
                entry["gpt_fix_attempted"] = gpt_fix
                entry["fix_status"] = fix_status
                entry["fix_log"] = fix_log or {}
                updated = True

        if updated:
            with open(self.report_path, "w") as f:
                json.dump(data, f, indent=2)
