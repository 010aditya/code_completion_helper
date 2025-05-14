import os
import re

class TestGeneratorAgent:
    def __init__(self, migrated_dir):
        self.migrated_dir = migrated_dir

    def generate_for_service(self, service_path):
        if not service_path.endswith(".java"):
            return

        test_dir = os.path.join(self.migrated_dir, "generated_tests")
        os.makedirs(test_dir, exist_ok=True)

        service_file = os.path.join(self.migrated_dir, service_path)
        if not os.path.exists(service_file):
            print(f"⚠️ Service file not found: {service_file}")
            return

        with open(service_file, "r") as f:
            code = f.read()

        class_name_match = re.search(r"public\s+class\s+(\w+)", code)
        if not class_name_match:
            print(f"⚠️ Could not find class name in {service_path}")
            return

        class_name = class_name_match.group(1)
        test_class_name = f"{class_name}Test"
        test_path = os.path.join(test_dir, f"{test_class_name}.java")

        test_code = f"""
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class {test_class_name} {{

    @Test
    void sampleTest() {{
        // TODO: replace with meaningful test
        assertTrue(true);
    }}
}}
"""
        with open(test_path, "w") as f:
            f.write(test_code)
        print(f"✅ Test case generated: {test_path}")
