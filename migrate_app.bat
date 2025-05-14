@echo off
set APP_NAME=%1

if "%APP_NAME%"=="" (
  echo ❗ Usage: migrate_app.bat app_name
  exit /b 1
)

echo 📦 Running EAR migration for %APP_NAME%...
python cli\migrate.py ^
  --legacy legacy_apps\%APP_NAME%.ear ^
  --migrated migrated_apps\%APP_NAME%.ear ^
  --mapping mappings\%APP_NAME%-ear-mapping.json ^
  --reference reference_apps\promoted

echo ✅ EAR complete. Using as reference for WAR...

python cli\migrate.py ^
  --legacy legacy_apps\%APP_NAME%.war ^
  --migrated migrated_apps\%APP_NAME%.war ^
  --mapping mappings\%APP_NAME%-war-mapping.json ^
  --reference-ear migrated_apps\%APP_NAME%.ear
