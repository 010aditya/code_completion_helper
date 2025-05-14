import os
import sys
import glob
from dotenv import load_dotenv
load_dotenv()

# Allow sibling module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.fix_and_compile import FixAndCompileAgent
from agents.build_validator import BuildValidatorAgent
from agents.context_stitcher import ContextStitcherAgent
from agents.package_structure_normalizer import PackageStructureNormalizerAgent
from agents.service_to_controller import ServiceToControllerAgent
from agents.framework_injection import FrameworkInjectionAgent
from agents.mapping_verifier import MappingVerifierAgent
from agents.retry_agent import RetryAgent
from agents.test_generator import TestGeneratorAgent
from agents.reference_promoter import ReferencePromoterAgent
from agents.embedding_indexer import EmbeddingIndexerAgent
from agents.rag_context_retriever import RAGContextRetrieverAgent
from agents.jsp_to_thymeleaf_converter import JspToThymeleafConverterAgent
from agents.struts_to_spring_controller import StrutsToSpringControllerAgent
from agents.metadata_agent import MetadataAgent

def find_java_root(base_path):
    """Find src/main/java/ path if exists"""
    java_path = os.path.join(base_path, "src", "main", "java")
    return java_path if os.path.exists(java_path) else base_path

def find_thymeleaf_root(base_path):
    """Find src/main/resources/templates/ path if exists"""
    tpl_path = os.path.join(base_path, "src", "main", "resources", "templates")
    return tpl_path if os.path.exists(tpl_path) else os.path.join(base_path, "templates")

def find_jsp_input_dir(base_path):
    """Try common JSP locations"""
    candidates = [
        os.path.join(base_path, "webapp"),
        os.path.join(base_path, "src", "main", "webapp"),
        os.path.join(base_path, "src", "main", "webapp", "WEB-INF", "jsp")
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

def run_migration_pipeline(legacy_dir, migrated_dir, mapping_path, reference_dir):
    migrated_code_root = find_java_root(migrated_dir)
    thymeleaf_output = find_thymeleaf_root(migrated_dir)

    print(f"🧠 Using code root: {migrated_code_root}")
    print(f"🎨 Thymeleaf templates: {thymeleaf_output}")

    print("✅ Verifying mappings...")
    mappings = MappingVerifierAgent(mapping_path).verify()

    print("📦 Normalizing package structure...")
    PackageStructureNormalizerAgent(migrated_code_root).normalize()

    print("🔁 Injecting modern framework references...")
    FrameworkInjectionAgent(migrated_code_root).inject_framework_references()

    print("🔧 Generating missing controllers for services...")
    ServiceToControllerAgent(migrated_code_root).generate_missing_controllers()

    print("📤 Migrating Struts XML to Spring controllers...")
    struts_config = os.path.join(legacy_dir, "WEB-INF", "struts-config.xml")
    if os.path.exists(struts_config):
        StrutsToSpringControllerAgent(struts_config, legacy_dir, migrated_code_root).migrate()
    else:
        print("🟡 No struts-config.xml found.")

    jsp_input_dir = find_jsp_input_dir(legacy_dir)
    if jsp_input_dir:
        jsp_files = glob.glob(f"{jsp_input_dir}/**/*.jsp", recursive=True)
        if jsp_files:
            print(f"🔄 Found {len(jsp_files)} JSP files in {jsp_input_dir}. Converting to Thymeleaf...")
            JspToThymeleafConverterAgent(jsp_input_dir, thymeleaf_output).convert_all()
        else:
            print("🟡 No JSP files found.")
    else:
        print("🟡 No JSP folder detected.")

    print("🧠 Fixing broken files with GPT + legacy context...")
    stitcher = ContextStitcherAgent(legacy_dir)
    fixer = FixAndCompileAgent(legacy_dir, migrated_code_root)
    for m in mappings:
        fixer.fix_file(m["targetPath"], stitcher)

    print("🧪 Validating compiled output...")
    results = BuildValidatorAgent(migrated_code_root).validate()

    print("🔁 Retrying failed GPT fixes...")
    RetryAgent("logs/fix_history", legacy_dir, migrated_code_root).retry_all_failures()

    print("🧪 Generating unit tests for services...")
    test_agent = TestGeneratorAgent(migrated_code_root)
    for m in mappings:
        if "Service" in m["targetPath"]:
            test_agent.generate_for_service(m["targetPath"])

    print("🏷 Annotating metadata...")
    for m in mappings:
        MetadataAgent().annotate(m["targetPath"], "post-migration")

    print("🚀 Promoting successful fixes as reference examples...")
    ReferencePromoterAgent().promote_successful_fixes()

    print("📡 Indexing embeddings for promoted references...")
    EmbeddingIndexerAgent(reference_dir).index_all()

    print("✅ Migration pipeline complete.")
