import os
import javalang

class ContextStitcherAgent:
    def __init__(self, legacy_dir):
        self.legacy_dir = legacy_dir

    def get_context_for_file(self, target_path: str) -> str:
        """
        Returns stitched context from legacy Java files that match the class name of the target_path.
        """
        class_name = os.path.basename(target_path).replace(".java", "")
        stitched_methods = []

        for root, _, files in os.walk(self.legacy_dir):
            for file in files:
                if not file.endswith(".java"):
                    continue
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        code = f.read()
                    tree = javalang.parse.parse(code)

                    for _, node in tree.filter(javalang.tree.ClassDeclaration):
                        if node.name == class_name:
                            stitched_methods.extend(self.extract_methods_from_class(node))
                except Exception as e:
                    continue  # skip files that fail parsing

        if not stitched_methods:
            return f"// No stitched legacy methods found for class {class_name}"
        return "\n\n".join(stitched_methods)

    def extract_methods_from_class(self, class_node):
        methods = []
        for method in class_node.methods:
            try:
                params = ", ".join(p.type.name for p in method.parameters)
                signature = f"{method.name}({params})"
                body = "\n".join(str(stmt) for stmt in method.body or [])
                methods.append(f"// Method: {signature}\n{body}")
            except Exception as e:
                continue
        return methods
