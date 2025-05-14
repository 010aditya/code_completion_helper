from dotenv import load_dotenv
load_dotenv()

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

def run_migration_pipeline(legacy_dir, migrated_dir, mapping_path, reference_dir):
    print("✅ Verifying mappings...")
    mappings = MappingVerifierAgent(mapping_path).verify()

    print("📦 Normalizing package structure...")
    PackageStructureNormalizerAgent(migrated_dir).normalize()

    print("🔁 Injecting modern framework references...")
    FrameworkInjectionAgent(migrated_dir).inject_framework_references()

    print("🔧 Generating missing controllers for services...")
    ServiceToControllerAgent(migrated_dir).generate_missing_controllers()

    print("📤 Migrating Struts XML to Spring controllers...")
    struts_config = "struts-config.xml"
    if struts_config:
        StrutsToSpringControllerAgent(struts_config, legacy_dir, migrated_dir).migrate()

    print("🧠 Fixing broken files with GPT + legacy context...")
    stitcher = ContextStitcherAgent(legacy_dir)
    fixer = FixAndCompileAgent(legacy_dir, migrated_dir)
    for m in mappings:
        fixer.fix_file(m["targetPath"], stitcher)

    print("🧪 Validating compiled output...")
    results = BuildValidatorAgent(migrated_dir).validate()

    print("🔁 Retrying failed GPT fixes...")
    RetryAgent("logs/fix_history", legacy_dir, migrated_dir).retry_all_failures()

    print("🧪 Generating unit tests for services...")
    test_agent = TestGeneratorAgent(migrated_dir)
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
