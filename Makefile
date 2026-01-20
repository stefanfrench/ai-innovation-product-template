# CapStack Makefile
# Common commands for development

.PHONY: help dev backend frontend install test lint clean docker-up docker-down

# Default target
help:
	@echo "CapStack - AI Product Innovation Template"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Development:"
	@echo "  dev          Start both backend and frontend (Docker)"
	@echo "  backend      Start backend only (local)"
	@echo "  frontend     Start frontend only (local)"
	@echo "  install      Install all dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test         Run all tests"
	@echo "  test-backend Run backend tests"
	@echo "  lint         Lint all code"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up    Start all services with Docker"
	@echo "  docker-down  Stop all Docker services"
	@echo "  docker-build Build Docker images"
	@echo ""
	@echo "Utilities:"
	@echo "  clean        Remove generated files"
	@echo "  db-reset     Reset the database"

# === Development ===

# Start everything with Docker (recommended)
dev:
	docker compose up

# Start backend locally (requires Python 3.11+ and UV)
backend:
	cd backend && uvicorn app.main:app --reload --port 8000

# Start frontend locally (requires Node.js 20+)
frontend:
	cd frontend && npm run dev

# Install all dependencies
install:
	cd backend && pip install uv && uv pip install --system -e ".[dev]"
	cd frontend && npm install

# === Testing ===

test: test-backend

test-backend:
	cd backend && pytest -v

lint:
	cd backend && ruff check .
	cd frontend && npm run lint

# === Docker ===

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-build:
	docker compose build

docker-logs:
	docker compose logs -f

# === Utilities ===

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	rm -f backend/*.db

db-reset:
	rm -f backend/*.db
	@echo "Database reset. It will be recreated on next backend start."
