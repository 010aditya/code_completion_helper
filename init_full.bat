@echo off

echo Creating virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt

echo Running migration pipeline...
python cli\migrate.py ^
  --legacy legacy_codebase ^
  --migrated migrated_codebase ^
  --mapping mapping.json ^
  --reference reference_apps\promoted
