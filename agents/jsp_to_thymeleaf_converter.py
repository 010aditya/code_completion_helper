import os
import re

class JspToThymeleafConverterAgent:
    def __init__(self, jsp_dir, output_dir):
        self.jsp_dir = jsp_dir
        self.output_dir = output_dir

    def convert_all(self, preview_mode=False):
        converted_count = 0
        for root, _, files in os.walk(self.jsp_dir):
            for file in files:
                if file.endswith(".jsp"):
                    input_path = os.path.join(root, file)
                    relative_path = os.path.relpath(input_path, self.jsp_dir)
                    output_path = os.path.join(self.output_dir, relative_path).replace(".jsp", ".html")
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

                    with open(input_path, "r", encoding="utf-8") as f:
                        jsp_content = f.read()

                    thymeleaf_content = self._convert_jsp_to_thymeleaf(jsp_content)

                    if preview_mode:
                        print(f"\n👀 Preview: {file}")
                        print(thymeleaf_content[:500])
                    else:
                        with open(output_path, "w", encoding="utf-8") as f:
                            f.write(thymeleaf_content)
                        print(f"✅ Converted: {input_path} → {output_path}")
                        converted_count += 1

        if not preview_mode:
            print(f"\n🧾 {converted_count} JSP files converted to Thymeleaf.\n")
        else:
            print(f"\n🔍 Preview mode completed for {converted_count} JSP files.\n")

    def _convert_jsp_to_thymeleaf(self, content):
        # Convert <c:forEach>
        content = re.sub(
            r'<c:forEach var="(\w+)" items="\$\{(\w+)}">',
            r'<div th:each="\1 : \${\2}">', content
        )
        content = content.replace("</c:forEach>", "</div>")

        # Convert <c:if>
        content = re.sub(
            r'<c:if test="\$\{(.*?)}">',
            r'<div th:if="\1">', content
        )
        content = content.replace("</c:if>", "</div>")

        # Convert ${...} to [[${...}]]
        content = re.sub(r"\$\{(.*?)}", r"[[${\1}]]", content)

        # Basic <form> replacement
        content = content.replace(
            "<form", "<form th:action=\"@{/submit}\" th:object=\"${form}\""
        )

        return content
