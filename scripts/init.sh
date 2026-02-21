#!/usr/bin/env bash
#
# Rename this template project to your own name.
# Usage: ./scripts/init.sh my-project-name
#
set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: ./scripts/init.sh <project-name>"
  echo "Example: ./scripts/init.sh my-ai-app"
  exit 1
fi

NEW_NAME="$1"
NEW_NAME_LOWER=$(echo "$NEW_NAME" | tr '[:upper:]' '[:lower:]')

echo "Renaming project to: $NEW_NAME"

FILES=(
  "backend/pyproject.toml"
  "backend/app/__init__.py"
  "backend/app/main.py"
  "backend/app/core/config.py"
  "backend/app/api/health.py"
  "frontend/package.json"
  "docker-compose.yml"
  ".env.example"
  ".github/workflows/ci.yml"
  ".github/workflows/deploy-azure.yml"
  "README.md"
)

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
      sed -i '' "s/capstack/$NEW_NAME_LOWER/gI" "$file" 2>/dev/null || \
      sed -i '' -e "s/capstack/$NEW_NAME_LOWER/g" -e "s/CapStack/$NEW_NAME/g" "$file"
    else
      sed -i "s/capstack/$NEW_NAME_LOWER/gI" "$file" 2>/dev/null || \
      sed -i -e "s/capstack/$NEW_NAME_LOWER/g" -e "s/CapStack/$NEW_NAME/g" "$file"
    fi
    echo "  Updated $file"
  fi
done

echo ""
echo "Done! Next steps:"
echo "  1. cp .env.example .env"
echo "  2. Add your API keys to .env"
echo "  3. docker compose up"
