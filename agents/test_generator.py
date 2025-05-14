import os
import openai

class TestGeneratorAgent:
    def __init__(self, migrated_dir, output_dir="generated_tests", api_key=None):
        self.migrated_dir = migrated_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def generate_for_service(self, service_file):
        service_path = os.path.join(self.migrated_dir, service_file)
        if not os.path.exists(service_path):
            return

        with open(service_path, "r") as f:
            code = f.read()

        prompt = f"""
You are an expert Java developer. Write JUnit5 test cases for the following Spring Boot service class.

Class:
{code}

Include imports and assume Mockito where necessary. Return only Java test code.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1500
            )
            test_code = response.choices[0].message.content.strip()
            test_path = os.path.join(self.output_dir, f"Test{os.path.basename(service_file)}")
            with open(test_path, "w") as tf:
                tf.write(test_code)
        except Exception as e:
            print(f"[TestGeneratorAgent] Failed for {service_file}: {e}")
