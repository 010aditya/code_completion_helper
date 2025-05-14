import os
import xml.etree.ElementTree as ET

class StrutsToSpringControllerAgent:
    def __init__(self, struts_config_path, legacy_dir, output_dir):
        self.struts_config_path = struts_config_path
        self.legacy_dir = legacy_dir
        self.output_dir = output_dir

    def migrate(self):
        actions = self._parse_struts_actions()
        for action in actions:
            controller_class = action["type"].split(".")[-1].replace("Action", "Controller")
            service_class = controller_class.replace("Controller", "Service")
            method_name = "handle" + controller_class.replace("Controller", "")
            view_name = action["forwards"].get("success", "index").replace(".jsp", "")
            form = action.get("name", "GenericForm")

            controller_code = f"""package com.migrated.controller;

import com.migrated.dto.{form};
import com.migrated.service.{service_class};
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/{view_name}")
public class {controller_class} {{

    private final {service_class} service;

    public {controller_class}({service_class} service) {{
        this.service = service;
    }}

    @PostMapping
    public String {method_name}(@ModelAttribute {form} form, Model model) {{
        Object result = service.{method_name}(form);
        model.addAttribute("result", result);
        return "{view_name}";
    }}
}}"""

            service_code = f"""package com.migrated.service;

import com.migrated.dto.{form};
import org.springframework.stereotype.Service;

@Service
public class {service_class} {{

    public Object {method_name}({form} form) {{
        // Migrate logic from execute() here if available
        return null;
    }}
}}"""

            os.makedirs(os.path.join(self.output_dir, "controller"), exist_ok=True)
            os.makedirs(os.path.join(self.output_dir, "service"), exist_ok=True)
            with open(os.path.join(self.output_dir, "controller", f"{controller_class}.java"), "w") as fc:
                fc.write(controller_code)
            with open(os.path.join(self.output_dir, "service", f"{service_class}.java"), "w") as fs:
                fs.write(service_code)

    def _parse_struts_actions(self):
        tree = ET.parse(self.struts_config_path)
        root = tree.getroot()
        actions = []
        for action in root.findall("action"):
            forwards = {fw.attrib['name']: fw.attrib['path'] for fw in action.findall("forward")}
            actions.append({
                "path": action.attrib.get("path", ""),
                "name": action.attrib.get("name", ""),
                "type": action.attrib.get("type", ""),
                "forwards": forwards
            })
        return actions
