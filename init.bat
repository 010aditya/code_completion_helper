@echo off
python cli\migrate.py --legacy legacy_codebase --migrated migrated_codebase --mapping mapping.json --reference reference_apps
