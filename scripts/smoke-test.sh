#!/usr/bin/env bash
#
# Smoke test for deployed or local instance.
# Usage: ./scripts/smoke-test.sh [base-url]
# Default: http://localhost:8000
#
set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"
PASSED=0
FAILED=0

check() {
  local name="$1"
  local method="$2"
  local url="$3"
  local expected_status="$4"
  local body="${5:-}"

  local args=(-s -o /dev/null -w "%{http_code}" -X "$method")
  if [ -n "$body" ]; then
    args+=(-H "Content-Type: application/json" -d "$body")
  fi

  local status
  status=$(curl "${args[@]}" "$url")

  if [ "$status" = "$expected_status" ]; then
    echo "  PASS  $name (HTTP $status)"
    PASSED=$((PASSED + 1))
  else
    echo "  FAIL  $name (expected $expected_status, got $status)"
    FAILED=$((FAILED + 1))
  fi
}

echo "Smoke testing: $BASE_URL"
echo "---"

check "Health check"      GET    "$BASE_URL/health"      200
check "Root endpoint"      GET    "$BASE_URL/"            200
check "List items"         GET    "$BASE_URL/api/items"   200
check "Create item"        POST   "$BASE_URL/api/items"   201  '{"name":"smoke-test","description":"auto"}'

# Clean up: find and delete the item we just created
ITEM_ID=$(curl -s "$BASE_URL/api/items" | python3 -c "
import sys, json
items = json.load(sys.stdin)
for item in items:
    if item['name'] == 'smoke-test':
        print(item['id'])
        break
" 2>/dev/null || echo "")

if [ -n "$ITEM_ID" ]; then
  check "Delete item"      DELETE "$BASE_URL/api/items/$ITEM_ID" 204
fi

echo "---"
echo "Results: $PASSED passed, $FAILED failed"

if [ "$FAILED" -gt 0 ]; then
  exit 1
fi
