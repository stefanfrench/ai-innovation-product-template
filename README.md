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
# Edit .env -- add your Azure OpenAI (or OpenAI) API key
```

### 3. Run

```bash
docker compose up
```

That's it. Open:
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

> **Database:** Local dev uses SQLite (zero setup). For production, add a managed Postgres instance and set `DATABASE_URL` -- the backend handles both automatically.

### Running without Docker

First, install [uv](https://docs.astral.sh/uv/) (one-time):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then:

```bash
# Backend (Python 3.11+)
cd backend
uv venv --python 3.12 .venv
# macOS/Linux: source .venv/bin/activate
# Windows:     .venv\Scripts\activate
uv pip install -e ".[dev]"
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
│   │   │   └── llm.py      # OpenAI / Azure OpenAI client
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
├── BRANDING.md             # Colour, typography & component reference
├── docker-compose.yml      # Local development
├── railway.json            # Railway multi-service config
└── .env.example           # Environment template
```

---

## LLM Integration

Uses the **OpenAI SDK** directly -- works with both Azure OpenAI (recommended) and OpenAI.

```bash
# Azure OpenAI (recommended)
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
LLM_MODEL=gpt-4o-mini          # your deployment name

# Or plain OpenAI
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
```

Usage in code:

```python
from app.core.llm import llm_complete, llm_stream

response = await llm_complete("Explain quantum computing")

async for chunk in llm_stream("Tell me a story"):
    print(chunk)
```

---

## Branding

The frontend uses **Capgemini brand colours** and the **Ubuntu** typeface. All tokens are defined in `frontend/tailwind.config.js` and ready-made component classes (`.btn-primary`, `.card`, `.input`) are in `frontend/src/style.css`.

See **[BRANDING.md](BRANDING.md)** for the full colour palette, typography rules, component examples, and do's/don'ts -- useful as a reference when building new pages or prompting AI tools to generate UI.

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

1. Create a new project on [railway.com](https://railway.com), deploy from your GitHub repo
2. Add a **second service** from the Architecture view (same repo) -- one for backend, one for frontend
3. Set **Root Directory** in each service's Settings: `backend` and `frontend` respectively. Railway auto-detects the Dockerfiles.
4. Add a **Postgres** plugin from the Architecture view -- Railway gives you a `DATABASE_URL` automatically. Link it to the backend service.
5. Add variables on the **backend** service: `LLM_MODEL` and your LLM API key (see `.env.example`)
6. Add one variable on the **frontend** service: `BACKEND_URL` = `http://<backend-service-name>.railway.internal:8000` (find the name under Settings > Private Networking > DNS)
7. Generate a **public domain** for each service under Settings > Networking (target port: `8000` for backend, `80` for frontend)

Railway auto-deploys on every push to `main`.

> **Note:** The backend listens on a hardcoded port 8000 -- do not use Railway's `${{service.PORT}}` reference variable. If `npm ci` fails, run `npm install` in `frontend/` locally and push the updated lockfile.

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
| | OpenAI SDK | Azure OpenAI / OpenAI integration |
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
| `LLM_MODEL` | Model / deployment name | gpt-4o-mini |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI key | - |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | - |
| `OPENAI_API_KEY` | OpenAI API key (alternative) | - |
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
