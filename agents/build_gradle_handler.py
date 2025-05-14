import os
import xml.etree.ElementTree as ET

class BuildGradleHandler:
    def __init__(self, legacy_dir, migrated_dir):
        self.legacy_dir = legacy_dir
        self.migrated_dir = migrated_dir
        self.gradle_path = os.path.join(migrated_dir, "build.gradle")

    def ensure_gradle_file(self):
        if os.path.exists(self.gradle_path):
            print("ℹ️ build.gradle already exists. Attempting patch.")
            self.patch_existing_gradle()
        elif self.generate_from_pom():
            print("✅ build.gradle generated from pom.xml.")
        else:
            self.generate_default()
            print("✅ Default build.gradle generated.")

    def patch_existing_gradle(self):
        with open(self.gradle_path, "r") as f:
            content = f.read()

        updated = False
        if "spring-boot-starter-web" not in content:
            content += "\nimplementation 'org.springframework.boot:spring-boot-starter-web'"
            updated = True
        if "org.springframework.boot" not in content:
            content = content.replace(
                "plugins {",
                "plugins {\n    id 'org.springframework.boot' version '3.2.2'\n    id 'io.spring.dependency-management' version '1.1.4'"
            )
            updated = True

        if updated:
            with open(self.gradle_path, "w") as f:
                f.write(content)
            print("✅ build.gradle patched with missing Spring Boot entries.")
        else:
            print("✅ build.gradle is complete. No patching needed.")

    def generate_from_pom(self):
        pom_path = os.path.join(self.legacy_dir, "pom.xml")
        if not os.path.exists(pom_path):
            return False

        try:
            tree = ET.parse(pom_path)
            root = tree.getroot()
            ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
            dependencies = root.find('m:dependencies', ns)

            gradle_deps = []
            if dependencies is not None:
                for dep in dependencies.findall('m:dependency', ns):
                    group = dep.find('m:groupId', ns).text
                    artifact = dep.find('m:artifactId', ns).text
                    version = dep.find('m:version', ns)
                    version_text = version.text if version is not None else 'latest.release'
                    gradle_deps.append(f"implementation '{group}:{artifact}:{version_text}'")

            with open(self.gradle_path, "w") as f:
                f.write(self._gradle_template(gradle_deps))
            return True

        except Exception as e:
            print(f"❌ Failed to parse pom.xml: {e}")
            return False

    def generate_default(self):
        with open(self.gradle_path, "w") as f:
            f.write(self._gradle_template())

    def _gradle_template(self, extra_deps=None):
        extra = '\n    '.join(extra_deps) if extra_deps else ''
        return f"""
plugins {{
    id 'java'
    id 'org.springframework.boot' version '3.2.2'
    id 'io.spring.dependency-management' version '1.1.4'
}}

group = 'com.migrated'
version = '0.0.1-SNAPSHOT'
sourceCompatibility = '21'

repositories {{
    mavenCentral()
}}

dependencies {{
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.boot:spring-boot-starter-validation'
    implementation 'org.springframework.boot:spring-boot-starter-aop'
    runtimeOnly 'com.h2database:h2'
    runtimeOnly 'org.postgresql:postgresql'
    runtimeOnly 'mysql:mysql-connector-java'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    {extra}
}}

test {{
    useJUnitPlatform()
}}
"""
