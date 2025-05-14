# 🧠 Migration Assist Post-Processor

An end-to-end AI-enhanced post-processing tool that takes **partially migrated Java applications** and transforms them into **clean, compilable, Spring Boot-compliant codebases** — with minimal manual effort.

---

## ✅ What This Tool Does

> You’ve run a migration tool (like Azure OpenAI or GPT-4o based transformer).  
> Now you’re left with:
- Broken references
- Uncompiled classes
- Missing methods or controllers
- Outdated JSPs
- Legacy framework classes

This tool:
- 🧠 Uses GPT-4o + legacy context (via AST) to fix broken files
- 🔧 Generates missing components (controllers, tests, Thymeleaf pages)
- 📦 Injects enterprise framework replacements
- 📡 Indexes reference examples to enable semantic lookups
- ✅ Outputs a buildable, QA-reviewed Spring Boot codebase

---

## 🗺️ Logical Migration Flow

```
INPUTS:
- legacy_codebase/
- migrated_output/
- mapping.json
- reference_apps/

PHASE 1: Setup
1. Verify file mappings
2. Normalize packages
3. Inject Spring framework references
4. Generate missing @Controllers

PHASE 2: Legacy Fix
5. Convert JSP → Thymeleaf (if any)
6. Convert struts-config.xml → @Controller + @Service
7. Fix broken migrated classes using GPT + legacy context (AST)

PHASE 3: QA + Test
8. Validate compilation using javac
9. Retry failed fixes
10. Generate unit test stubs

PHASE 4: RAG Support
11. Promote successful fixes to reference apps
12. Embed all examples for future semantic lookups

PHASE 5: Manual Review (optional)
13. Launch QA dashboard and annotate
```

---

## 📂 Folder Structure

```
.
├── agents/                     # Modular AI + AST agents
├── cli/migrate.py             # CLI runner
├── cli/suggest_framework_mapping.py  # Class mapping suggester
├── core/orchestrator.py       # Full pipeline logic
├── config/framework_mapping.json     # Manual or suggested class replacements
├── data/migration_report.json # Full audit + QA info
├── logs/fix_history/          # GPT fix history per file
├── reference_apps/promoted/   # Embedded good examples
├── ui/qa_dashboard.py         # Streamlit-based review UI
├── requirements.txt
├── .env
```

---

## 🚀 How to Run (Step-by-Step)

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure `.env`

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
PYTHONPATH=.
```

### Step 3: Run migration pipeline

```bash
python cli/migrate.py \
  --legacy legacy_codebase \
  --migrated migrated_output \
  --mapping mapping.json \
  --reference reference_apps/promoted
```

### Step 4: Run QA Dashboard

```bash
streamlit run ui/qa_dashboard.py
```

---

## 🔧 Features & Agents

| Feature | Description |
|--------|-------------|
| `FixAndCompileAgent` | Fixes migrated files using GPT + legacy AST |
| `ContextStitcherAgent` | Parses legacy `.java` files using `javalang` |
| `BuildValidatorAgent` | Compiles Java files using `javac` |
| `RetryAgent` | Automatically retries failed GPT completions |
| `TestGeneratorAgent` | Generates unit tests using GPT |
| `JspToThymeleafConverterAgent` | Converts JSPs to Thymeleaf |
| `StrutsToSpringControllerAgent` | Generates `@Controller` and `@Service` from XML |
| `FrameworkInjectionAgent` | Replaces legacy class references using `framework_mapping.json` |
| `ServiceToControllerAgent` | Detects missing controllers and generates them |
| `ReferencePromoterAgent` | Adds fixed files to reusable embeddings |
| `EmbeddingIndexerAgent` | Builds FAISS index of reference pairs |
| `RAGContextRetrieverAgent` | Fetches semantically similar examples |
| `MetadataAgent` | Annotates QA status, audit tags |
| `FrameworkMappingSuggesterAgent` | Suggests mappings between legacy and Spring Boot frameworks |

---

## 🔬 Example Use Cases

- 🧩 Fix "method not found" errors by pulling from legacy context
- 🛠 Convert JSPs to `templates/*.html`
- 📡 Promote good fixes for future GPT context
- 📊 Run full QA checklist in browser
- 🔁 Inject modern equivalents of legacy framework classes

---

## 🧪 QA Dashboard Guide

```bash
streamlit run ui/qa_dashboard.py
```

You’ll be able to:
- ✅ Mark compiles OK
- ✅ Confirm controller/service separation
- ✅ Check if DTOs used
- 📝 Add notes
- 💾 Save back to `migration_report.json`

---

## 🧰 Optional Scripts

```bash
./init_full.sh       # Create venv, install, run CLI
init_full.bat        # Windows version
```

---

## ⚠️ Known Limitations

- Fixes are best effort — edge cases still require dev review
- Token size limits may chunk long classes (but chunking is optimized)
- Relies on good examples in `reference_apps/` for high RAG quality

---

## 📤 To Extend This

- Add your own agents in `agents/`
- Customize `framework_mapping.json` or auto-suggest via CLI
- Wire into your CI/CD using `migrate.py` + `migration_report.json`

---

## ✅ You’re Ready

Run:

```bash
python cli/migrate.py ...
```

Then:

```bash
streamlit run ui/qa_dashboard.py
```

Enjoy clean, compiled, AI-enhanced Java code — ready for Spring Boot.
