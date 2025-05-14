import os
import javalang

class ContextStitcherAgent:
    def __init__(self, legacy_dir):
        self.legacy_dir = legacy_dir

    def get_stitched_context(self, target_file):
        class_name = os.path.basename(target_file).replace(".java", "")
        stitched_methods = []

        for root, _, files in os.walk(self.legacy_dir):
            for file in files:
                if file.endswith(".java"):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r") as f:
                            code = f.read()
                        tree = javalang.parse.parse(code)
                        for _, node in tree.filter(javalang.tree.ClassDeclaration):
                            if class_name in node.name:
                                stitched_methods.extend(self.extract_methods_from_class(node))
                    except:
                        continue

        return "\n\n".join(stitched_methods)

    def extract_methods_from_class(self, class_node):
        methods = []
        for method in class_node.methods:
            signature = method.name + "(" + ", ".join(p.type.name for p in method.parameters) + ")"
            body = "\n".join(str(stmt) for stmt in method.body if stmt)
            methods.append(f"// {signature}\n{body}")
        return methods
