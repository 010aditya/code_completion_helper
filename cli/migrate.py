import argparse
from dotenv import load_dotenv
load_dotenv()

from core.orchestrator import run_migration_pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the migration pipeline")
    parser.add_argument("--legacy", required=True, help="Path to legacy codebase")
    parser.add_argument("--migrated", required=True, help="Path to output migrated codebase")
    parser.add_argument("--mapping", required=True, help="Path to mapping.json")
    parser.add_argument("--reference", help="Reference apps or promoted output (e.g. .ear)")
    parser.add_argument("--reference-ear", help="Optional .ear output to use as RAG priority for controller fixes")

    args = parser.parse_args()

    # Combine .ear and reference if both passed
    final_reference_dir = args.reference
    if args.reference_ear:
        print(f"📦 Including reference-ear context from: {args.reference_ear}")
        final_reference_dir = args.reference_ear

    run_migration_pipeline(
        legacy_dir=args.legacy,
        migrated_dir=args.migrated,
        mapping_path=args.mapping,
        reference_dir=final_reference_dir
    )
