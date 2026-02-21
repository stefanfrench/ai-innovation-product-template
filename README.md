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
./scripts/init.sh your-project-name   # renames all internal references
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env` and add your LLM credentials:

```bash
# Azure OpenAI (recommended)
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
LLM_MODEL=gpt-4o-mini

# Or plain OpenAI
OPENAI_API_KEY=sk-...
```

> **Auth:** Set `API_KEY=your-secret` in `.env` to require an `X-API-Key` header on all `/api/*` routes. Leave it empty to disable (default).

### 3. Run

```bash
docker compose up
```

Open **http://localhost:5173** (frontend) and **http://localhost:8000/docs** (API docs, dev only).

> **Database:** Local dev uses SQLite (zero setup). For production, set `DATABASE_URL` to a Postgres connection string -- the backend handles both automatically.

### Running without Docker

Install [uv](https://docs.astral.sh/uv/) (one-time):

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

## Using the Template

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

### Add a database model

Add to `backend/app/db/models.py`:

```python
class YourModel(Base):
    __tablename__ = "your_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
```

Restart the backend -- tables are auto-created in development. For production, add [Alembic](https://alembic.sqlalchemy.org/) for migrations.

### Add a frontend page

1. Create `frontend/src/pages/YourPage.vue`
2. Add route in `frontend/src/router/index.ts`:

```typescript
{
  path: '/your-page',
  name: 'your-page',
  component: () => import('@/pages/YourPage.vue'),
}
```

### Use the LLM in backend code

```python
from app.core.llm import llm_complete, llm_stream

response = await llm_complete("Explain quantum computing")

async for chunk in llm_stream("Tell me a story"):
    print(chunk)
```

---

## Branding

The frontend uses Capgemini brand colours and the Ubuntu typeface. See **[BRANDING.md](BRANDING.md)** for the colour palette, typography, component classes, and do's/don'ts.

---

## Testing

```bash
cd backend && pytest -v          # Backend
cd frontend && npm test          # Frontend
./scripts/smoke-test.sh <url>    # Verify a deployment
```

---

## Deployment

### Railway

1. Create a new project on [railway.com](https://railway.com), deploy from your GitHub repo
2. Add a **second service** from the Architecture view (same repo) -- one for backend, one for frontend
3. Set **Root Directory** in each service's Settings: `backend` and `frontend` respectively
4. Add a **Postgres** plugin from the Architecture view -- Railway provides `DATABASE_URL` automatically. Link it to the backend service.
5. Add variables on the **backend** service: `LLM_MODEL` and your LLM API key (see `.env.example`)
6. Add one variable on the **frontend** service: `BACKEND_URL` = `http://<backend-service-name>.railway.internal:8000`
7. Generate a **public domain** for each service under Settings > Networking (target port: `8000` for backend, `80` for frontend)

Railway auto-deploys on every push to `main`.

> **Note:** The backend listens on port 8000 -- do not use Railway's `${{service.PORT}}` variable. If `npm ci` fails, run `npm install` locally in `frontend/` and push the updated lockfile.

### Azure Container Apps

Triggered manually from **Actions > Deploy to Azure > Run workflow**.

Prerequisites (one-time):

```bash
az group create -n myapp-rg -l uksouth
az acr create -n myappacr -g myapp-rg --sku Basic --admin-enabled
az containerapp env create -n capstack-env -g myapp-rg -l uksouth
```

GitHub secrets required: `AZURE_CREDENTIALS`, `ACR_LOGIN_SERVER`, `ACR_USERNAME`, `ACR_PASSWORD`, `AZURE_RESOURCE_GROUP`, `AZURE_LOCATION`.

---

## Project Structure

```
backend/                  FastAPI backend
  app/api/                Route handlers (health, items, llm)
  app/core/               Config, auth, database, LLM client
  app/db/                 SQLAlchemy models
  tests/                  Pytest tests

frontend/                 Vue 3 + TypeScript frontend
  src/components/         Reusable UI components
  src/composables/        Vue composables (useApi, useWebSocket)
  src/pages/              Route views
  src/router/             Vue Router config

scripts/
  init.sh                 Rename project from template
  smoke-test.sh           Verify a deployment

.github/workflows/
  ci.yml                  Tests, linting, Docker builds
  deploy-azure.yml        Azure Container Apps deployment

BRANDING.md               Colour & typography reference
docker-compose.yml        Local development
railway.json              Railway multi-service config
.env.example              All environment variables
```

---

<p align="center">
  Built with care by the <strong>AI Product Innovation</strong> team
</p>
