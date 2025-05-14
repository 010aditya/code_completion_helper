import streamlit as st
import json
import os

REPORT_PATH = "data/migration_report.json"

st.set_page_config(page_title="Migration QA Dashboard", layout="wide")
st.title("🚦 Migration QA Review Dashboard")

if not os.path.exists(REPORT_PATH):
    st.error("No migration report found. Please run the migration tool first.")
    st.stop()

with open(REPORT_PATH, "r") as f:
    data = json.load(f)

report = data.get("report", [])
metadata = data.get("metadata", {})

edited = []
st.markdown("### 📋 File Checklist")

for entry in report:
    col1, col2, col3 = st.columns([4, 2, 4])
    with col1:
        st.markdown(f"**`{entry['filename']}`**")
        st.text(f"Legacy: {entry.get('legacy_source_path', 'N/A')}")
        st.text(f"Compile: {entry['compilation']}")
    with col2:
        checklist = entry.get("qa_checklist", {})
        checklist['compiles'] = st.checkbox("✅ Compiles", value=checklist.get("compiles", False), key=entry['filename']+"_c")
        checklist['controller_present'] = st.checkbox("🧭 Controller", value=checklist.get("controller_present", False), key=entry['filename']+"_cp")
        checklist['service_separated'] = st.checkbox("🧩 Service Separated", value=checklist.get("service_separated", False), key=entry['filename']+"_ss")
        checklist['dto_used'] = st.checkbox("📦 DTO Used", value=checklist.get("dto_used", False), key=entry['filename']+"_dto")
        checklist['thymeleaf_ready'] = st.checkbox("🎨 Thymeleaf Ready", value=checklist.get("thymeleaf_ready", False), key=entry['filename']+"_th")
        checklist['manual_review_done'] = st.checkbox("👁 Manual Reviewed", value=checklist.get("manual_review_done", False), key=entry['filename']+"_mr")
        entry['qa_checklist'] = checklist
    with col3:
        entry['notes'] = st.text_area("📝 Notes", value=entry.get("notes", ""), key=entry['filename']+"_note")
    st.markdown("---")
    edited.append(entry)

if st.button("💾 Save Review Updates"):
    with open(REPORT_PATH, "w") as f:
        json.dump({"report": edited, "metadata": metadata}, f, indent=2)
    st.success("Review checklist updated!")
