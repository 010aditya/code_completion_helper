#!/bin/bash

echo "🔧 Creating virtual environment..."
python3 -m venv .venv

echo "✅ Activating virtual environment..."
source .venv/bin/activate

echo "📦 Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🚀 Running migration pipeline..."
python cli/migrate.py \
  --legacy legacy_codebase \
  --migrated migrated_codebase \
  --mapping mapping.json \
  --reference reference_apps/promoted
