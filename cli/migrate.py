import argparse
from dotenv import load_dotenv
load_dotenv()

from core.orchestrator import run_migration_pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the migration pipeline")
    parser.add_argument("--legacy", required=True, help="Path to legacy codebase")
    parser.add_argument("--migrated", required=True, help="Path to output migrated codebase")
    parser.add_argument("--mapping", required=True, help="Path to mapping.json")
    parser.add_argument("--reference", help="Optional path to reference_apps folder")
    args = parser.parse_args()

    run_migration_pipeline(
        legacy_dir=args.legacy,
        migrated_dir=args.migrated,
        mapping_path=args.mapping,
        reference_dir=args.reference
    )
