import os

class PackageStructureNormalizerAgent:
    def __init__(self, base_dir, base_package="com.migrated"):
        self.base_dir = base_dir
        self.base_package = base_package

    def normalize(self):
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(root, self.base_dir)
                    package_suffix = rel_path.replace(os.sep, ".").strip(".")
                    full_package = f"{self.base_package}.{package_suffix}" if package_suffix else self.base_package
                    package_declaration = f"package {full_package};\n\n"

                    try:
                        with open(file_path, "r") as f:
                            lines = f.readlines()

                        if not lines or not lines[0].strip().startswith("package "):
                            lines.insert(0, package_declaration)
                            with open(file_path, "w") as f:
                                f.writelines(lines)

                    except Exception as e:
                        print(f"[PackageStructureNormalizerAgent] Error processing {file_path}: {e}")
