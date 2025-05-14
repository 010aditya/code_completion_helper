# 🧠 Migration Assist Post-Processor – Full Workflow & Usage Guide

...

## 🔁 Clarification: What `.war` Means

❗ **NOTE**: In this tool, `.war` does NOT mean a packaged `.war` archive.

Instead:
- `--legacy` points to the legacy web application source (JSP, Struts, etc.)
- `--migrated` points to a **partially migrated Spring Boot/MVC/Thymeleaf codebase**
- This output may include:
  - `src/main/java/`
  - `src/main/resources/templates/`
  - `pom.xml` or `build.gradle`

...

## 🧠 Workflow Overview

...

## 📦 Step-by-Step Migration

1. ✅ **Migrate `.ear` first** — this gives you reusable `@Service`, `@Repository`, and common logic
2. ✅ **Migrate `.war` Spring output path** — the output folder from Migration Assist with partially converted Spring Boot code
3. ✅ The tool fixes and links `@Controllers` to `.ear` `@Services`
4. ✅ Review and QA in the dashboard

...

## 🛠 Auto-detecting Spring Roots

If your migrated output is a Spring Boot project (not a WAR):
- The tool will detect `src/main/java/`, `src/main/resources/templates/` automatically
- The agents will scan only relevant files under these directories

...

