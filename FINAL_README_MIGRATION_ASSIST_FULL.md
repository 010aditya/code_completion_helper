# 🧠 Migration Assist Tool — End-to-End Code Finalizer

A post-processing migration system for Java applications originally built with EJB, JSP, Struts, iBatis, and custom enterprise frameworks.

---

## ✅ Purpose

This tool takes partially migrated code (output from LLM-based tools like Migration Assist) and auto-fixes, completes, and validates it — producing a clean, modern Spring Boot + Thymeleaf architecture.

---

## 🗂 Folder Structure

```
.
├── agents/                     # All fix/validation/migration agents
├── cli/migrate.py             # CLI entrypoint
├── core/orchestrator.py       # Pipeline controller
├── config/framework_mapping.json  # Legacy-to-modern mapping rules
├── ui/qa_dashboard.py         # Streamlit-based checklist UI
├── logs/                      # Fix history + manual review tracking
├── data/                      # Output reports (e.g. migration_report.json)
├── reference_apps/promoted/   # Good legacy/migrated pairs for RAG
├── .env                       # API keys (e.g. OPENAI_API_KEY=sk-...)
├── init.sh / init.bat         # One-click run scripts
├── requirements.txt           # Python dependencies
├── README.md                  # You're here!
```

---

## 🚀 How It Works

### 🔁 Input Requirements

- ✅ Legacy source folder (pre-migration)
- ✅ Output folder (from migration tool like GPT, Azure OpenAI, etc.)
- ✅ mapping.json from Migration Assist (1:1 or 1:N source-target mapping)

### ⚙️ What This Tool Does

| Stage       | Description                                                         |
|-------------|---------------------------------------------------------------------|
| 🧠 Fix       | Uses GPT-4o and legacy context to fix broken or partial classes     |
| 🧩 Validate  | Compiles all `.java` files and flags errors                         |
| 🏷 Metadata  | Tracks fix history, review status, and manual QA                    |
| 📥 Retry     | Attempts to fix any failed GPT completions                          |
| 🔧 Promote   | Adds successful fixes as learnable reference pairs                  |
| 📈 Embed     | Uses sentence-transformers + FAISS for semantic retrieval           |
| 🛠 Migrate   | Converts JSP → Thymeleaf and Struts XML → Spring MVC                |
| 📤 QA        | Opens a UI dashboard to visually review all migration output        |

---

## 🧪 Quickstart

### 1. Install Python Requirements

```bash
pip install -r requirements.txt
```

### 2. Create `.env` file with your API key

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Run Migration Pipeline

```bash
python cli/migrate.py \
  --legacy ./legacy_codebase \
  --migrated ./migrated_output \
  --mapping ./mapping.json \
  --reference ./reference_apps/promoted
```

### 4. Launch QA Review Dashboard

```bash
streamlit run ui/qa_dashboard.py
```

---

## 🧠 Smart Agents (Plugins)

| Agent                         | Description                                                   |
|------------------------------|---------------------------------------------------------------|
| `FixAndCompileAgent`         | Uses GPT + legacy AST context to fix broken classes           |
| `BuildValidatorAgent`        | Compiles `.java` files using `javac`                          |
| `RetryAgent`                 | Re-attempts failed GPT completions                           |
| `ContextStitcherAgent`       | Pulls method-level legacy context                            |
| `CompletionAgent`            | Suggests missing methods from legacy class                   |
| `TestGeneratorAgent`         | Writes unit tests for migrated services                      |
| `StrutsToSpringControllerAgent` | Converts `struts-config.xml` to Spring MVC                |
| `JspToThymeleafConverterAgent` | Converts `.jsp` to `.html` with Thymeleaf                |
| `ServiceToControllerAgent`   | Detects and generates missing controllers for services       |
| `FrameworkInjectionAgent`    | Replaces old framework usage with modern Spring equivalents   |
| `ReferencePromoterAgent`     | Promotes successful GPT fixes into RAG reference set          |
| `EmbeddingIndexerAgent`      | Embeds approved examples for semantic retrieval               |
| `RAGContextRetrieverAgent`   | Retrieves similar examples during GPT fixing                  |
| `MetadataAgent`              | Logs QA status and notes per migrated file                    |

---

## 🧭 How to Review

Once the migration is complete, run the dashboard:

```bash
streamlit run ui/qa_dashboard.py
```

Mark off:
- Compiles successfully?
- Controller/Service separation correct?
- DTO used?
- Manual review done?

Then save. You can re-run as many times as needed.

---

## ⚠️ Limitations & Realistic Expectations

> ❌ This is not a silver bullet — but a **huge accelerator**.

- Complex business logic may still require developer refactoring
- Some build errors may require framework configuration
- You should have at least 1-2 migrated projects available as references
- It’s designed to cut down 80% of the manual work, not eliminate 100%

---

## 🧰 Dev Enablement

### Scripts

```bash
./init.sh           # Bash shortcut
init.bat            # Windows .bat runner
```

### .env Setup

```env
OPENAI_API_KEY=your-openai-key-here
PYTHONPATH=.
```

---

## 📃 License

MIT or enterprise internal use — customize as per your organization.

---

## 👨‍💻 Maintainer Notes

- Add `__init__.py` in `agents/` if you package this
- Set VS Code workspace `.env` to: `PYTHONPATH=${workspaceFolder}`
- Consider building a Docker wrapper for portability

---

## ✅ You're Ready!

If you’ve wired everything up and see the dashboard:
> 🎉 You now have a self-healing, RAG-powered, agent-driven, AI-assisted migration post-processor!
