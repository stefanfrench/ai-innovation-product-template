# AI Product Innovation Template

A full-stack starter for building AI-powered PoCs, fast.

> Built by the AI Product Innovation team at Capgemini Invent

---

## Quick Start

### 1. Create your project

Use this repo as a GitHub template, then rename it:

```bash
git clone https://github.com/your-org/your-project.git
cd your-project
./scripts/init.sh your-project-name
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env -- add your LLM API key (OpenAI, Azure OpenAI, or Anthropic)
```

### 3. Run

```bash
docker compose up
```

That's it. Open:
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

### Running without Docker

```bash
# Backend (Python 3.11+)
cd backend
pip install uv && uv pip install --system -e ".[dev]"
python -m uvicorn app.main:app --reload

# Frontend (Node.js 20+)
cd frontend
npm install
npm run dev
```

---

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # Route handlers
│   │   │   ├── health.py   # Health check (with DB status)
│   │   │   ├── items.py    # Example CRUD API
│   │   │   └── llm.py      # LLM endpoints + WebSocket
│   │   ├── core/           # Configuration & utilities
│   │   │   ├── auth.py     # API key auth (opt-in)
│   │   │   ├── config.py   # Environment settings
│   │   │   ├── database.py # SQLAlchemy async setup
│   │   │   └── llm.py      # LiteLLM integration
│   │   └── db/
│   │       └── models.py   # Database models
│   └── tests/              # Pytest tests
│
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── __tests__/     # Vitest tests
│   │   ├── components/     # Reusable UI components
│   │   ├── composables/    # Vue composables (useApi, useWebSocket)
│   │   ├── pages/          # Route views
│   │   └── router/         # Vue Router config
│   └── ...
│
├── scripts/
│   ├── init.sh            # Rename project from template
│   └── smoke-test.sh      # Verify a deployment works
│
├── .github/workflows/
│   ├── ci.yml             # Tests, linting, Docker builds
│   ├── deploy.yml         # Railway auto-deploy
│   └── deploy-azure.yml   # Azure Container Apps (manual trigger)
│
├── docker-compose.yml      # Local development
├── railway.json            # Railway multi-service config
└── .env.example           # Environment template
```

---

## LLM Integration

Uses **LiteLLM** for unified access to 100+ LLM providers. Set your provider in `.env`:

```bash
# OpenAI
LITELLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...

# Azure OpenAI
LITELLM_MODEL=azure/your-deployment-name
AZURE_API_KEY=...
AZURE_API_BASE=https://your-resource.openai.azure.com

# Anthropic
LITELLM_MODEL=claude-3-sonnet-20240229
ANTHROPIC_API_KEY=...

# Local (Ollama)
LITELLM_MODEL=ollama/llama2
```

Usage in code:

```python
from app.core.llm import llm_complete, llm_stream

response = await llm_complete("Explain quantum computing")

async for chunk in llm_stream("Tell me a story"):
    print(chunk)
```

---

## Authentication

Simple API key auth is built in but **off by default**. To enable it, set one environment variable:

```bash
API_KEY=your-secret-key-here
```

When set, all `/api/*` endpoints require an `X-API-Key` header. Health and root endpoints remain open. To disable, just leave `API_KEY` unset.

---

## Common Tasks

### Add a new API endpoint

1. Create `backend/app/api/your_endpoint.py`:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/your-route", tags=["your-tag"])

@router.get("")
async def your_endpoint():
    return {"message": "Hello!"}
```

2. Register in `backend/app/main.py`:

```python
from app.api import your_endpoint
app.include_router(your_endpoint.router, prefix="/api", dependencies=[Depends(verify_api_key)])
```

### Add a new database model

Add to `backend/app/db/models.py`:

```python
class YourModel(Base):
    __tablename__ = "your_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
```

Restart the backend -- tables are auto-created in development.

> For production, add [Alembic](https://alembic.sqlalchemy.org/) for proper migrations.

### Add a new frontend page

1. Create `frontend/src/pages/YourPage.vue`
2. Add route in `frontend/src/router/index.ts`:

```typescript
{
  path: '/your-page',
  name: 'your-page',
  component: () => import('@/pages/YourPage.vue'),
}
```

---

## Testing

```bash
# Backend
cd backend && pytest -v

# Frontend
cd frontend && npm test

# Smoke test a running instance
./scripts/smoke-test.sh                     # localhost:8000
./scripts/smoke-test.sh https://your-app.example.com  # deployed
```

---

## Deployment

### Railway

1. Create a project on [Railway](https://railway.app) and connect your GitHub repo
2. Railway will detect `railway.json` and create both services (backend + frontend)
3. Set environment variables on the **backend** service (from `.env.example`):
   - `DATABASE_URL`, `LITELLM_MODEL`, your LLM API key, etc.
4. Set one variable on the **frontend** service:
   - `BACKEND_URL` = `http://backend.railway.internal:${{backend.PORT}}`
   - (Use Railway's reference variable syntax to point to the backend's internal URL)
5. Optionally add `RAILWAY_TOKEN` to GitHub secrets for auto-deploy on push to `main`

### Azure Container Apps

Deployment is triggered manually from the GitHub Actions tab.

**Prerequisites** (one-time setup):

```bash
# Create resource group and container registry
az group create -n myapp-rg -l uksouth
az acr create -n myappacr -g myapp-rg --sku Basic --admin-enabled
az containerapp env create -n capstack-env -g myapp-rg -l uksouth
```

**GitHub secrets required:**

| Secret | Value |
|--------|-------|
| `AZURE_CREDENTIALS` | Output of `az ad sp create-for-rbac --sdk-auth` |
| `ACR_LOGIN_SERVER` | e.g. `myappacr.azurecr.io` |
| `ACR_USERNAME` | ACR admin username |
| `ACR_PASSWORD` | ACR admin password |
| `AZURE_RESOURCE_GROUP` | e.g. `myapp-rg` |
| `AZURE_LOCATION` | e.g. `uksouth` |

Then go to **Actions > Deploy to Azure > Run workflow**.

### Verify any deployment

```bash
./scripts/smoke-test.sh https://your-backend-url.example.com
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | FastAPI | Async Python web framework |
| | SQLAlchemy 2.0 | Async ORM with type hints |
| | LiteLLM | Unified LLM API (OpenAI, Azure, Anthropic, etc.) |
| | UV | Fast Python package manager |
| **Frontend** | Vue 3 | Progressive UI framework |
| | TypeScript | Type safety |
| | Vite | Build tool |
| | Tailwind CSS | Utility-first styling |
| | TanStack Query | Data fetching and caching |
| **Testing** | Pytest | Backend tests |
| | Vitest | Frontend tests |
| **DevOps** | Docker | Containerization |
| | GitHub Actions | CI/CD pipelines |
| | Railway | Deployment (quick/free) |
| | Azure Container Apps | Deployment (enterprise) |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | Environment (development/staging/production) | development |
| `DATABASE_URL` | Database connection string | SQLite (local) |
| `LITELLM_MODEL` | Default LLM model | gpt-4o-mini |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `AZURE_API_KEY` | Azure OpenAI key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `API_KEY` | API key auth (leave empty to disable) | - |
| `CORS_ORIGINS` | Allowed CORS origins | localhost |

See `.env.example` for all options.

---

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `cd backend && pytest` / `cd frontend && npm test`
4. Run linting: `cd backend && ruff check .` / `cd frontend && npm run lint`
5. Open a PR to `main`

---

<p align="center">
  Built with care by the <strong>AI Product Innovation</strong> team
</p>
