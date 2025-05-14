# 🚀 Migration Assist Post-Processor

End-to-end tool for finalizing Java migration from legacy technologies (EJB, JSP, Struts, iBatis) to Spring Boot + Thymeleaf.

## 💼 Structure

- `agents/` - Core intelligent agents (fix, validate, complete, convert)
- `core/` - Orchestrator that wires it all together
- `cli/` - Command-line entry point
- `ui/` - Streamlit QA dashboard
- `logs/` - Fix logs, manual review history
- `data/` - Final migration report
- `reference_apps/` - Learnable examples
- `config/` - Mapping and framework rules

## ⚙️ How to Run

### 1. Set up
```bash
pip install -r requirements.txt
```

### 2. Start Migration
```bash
python cli/migrate.py \
  --legacy legacy_codebase \
  --migrated migrated_codebase \
  --mapping mapping.json \
  --reference reference_apps
```

### 3. Review Output
```bash
streamlit run ui/qa_dashboard.py
```

## 🎯 Features

- Fixes broken classes using AST + GPT
- Moves logic from Struts actions to Spring controllers + services
- Converts JSP to Thymeleaf
- Adds missing controllers from services
- Injects modern framework usage
- Validates builds (`javac`, `gradle`)
- Tracks fix history, manual review
- Uses embeddings to improve future fixes

## ✅ Scripts

Use these scripts for convenience:
- `init.sh`: Bash startup
- `init.bat`: Windows batch startup
