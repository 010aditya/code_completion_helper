import argparse
from agents.framework_mapping_suggester import FrameworkMappingSuggesterAgent

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Suggest enterprise framework mappings")
    parser.add_argument("--legacy-fw", required=True, help="Path to legacy enterprise framework")
    parser.add_argument("--springboot-fw", required=True, help="Path to migrated Spring Boot framework")
    parser.add_argument("--output", default="config/suggested_framework_mapping.json", help="Path to save suggestions")
    args = parser.parse_args()

    agent = FrameworkMappingSuggesterAgent(
        legacy_dir=args.legacy_fw,
        springboot_dir=args.springboot_fw,
        output_path=args.output
    )

    suggestions = agent.suggest_mappings()
    print(f"✅ Suggested {len(suggestions)} mappings saved to {args.output}")
