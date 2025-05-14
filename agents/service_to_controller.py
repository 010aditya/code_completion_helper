import os

class ServiceToControllerAgent:
    def __init__(self, migrated_dir):
        self.migrated_dir = migrated_dir
        self.flagged_services = []

    def generate_missing_controllers(self):
        service_files = []
        controller_files = []

        for root, _, files in os.walk(self.migrated_dir):
            for file in files:
                if file.endswith(".java"):
                    if "Service" in file:
                        service_files.append((file, os.path.join(root, file)))
                    elif "Controller" in file:
                        controller_files.append(file)

        generated = []

        for service_file, service_path in service_files:
            controller_name = service_file.replace("Service", "Controller")
            if controller_name not in controller_files:
                service_class = service_file.replace(".java", "")
                controller_class = controller_name.replace(".java", "")
                method_name = "handle" + service_class.replace("Service", "")

                controller_code = f"""package com.migrated.controller;

import com.migrated.service.{service_class};
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/{method_name.lower()}")
public class {controller_class} {{

    private final {service_class} service;

    public {controller_class}({service_class} service) {{
        this.service = service;
    }}

    @PostMapping
    public String {method_name}(Model model) {{
        Object result = service.{method_name}();
        model.addAttribute("result", result);
        return "{method_name.lower()}";
    }}
}}"""

                controller_path = os.path.join(os.path.dirname(service_path), controller_name)
                with open(controller_path, "w") as f:
                    f.write(controller_code)

                generated.append(controller_path)
                self.flagged_services.append(service_class)

        return generated, self.flagged_services
