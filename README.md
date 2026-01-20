# 🚀 CapStack

**AI Product Innovation Template** - A full-stack starter for building AI-powered applications.

> Built by the AI Product Innovation team at Capgemini

---

## ⚡ Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone and enter the project
git clone https://github.com/stefanfrench/capstack.git
cd capstack

# Copy environment file and add your API keys
cp .env.example .env

# Start everything
docker compose up
```

That's it! Open:
- 🖥️ **Frontend**: http://localhost:5173
- 🔌 **API Docs**: http://localhost:8000/docs

### Option 2: Local Development

```bash
# Backend (Python 3.11+)
cd backend
pip install uv
uv pip install --system -e ".[dev]"
uvicorn app.main:app --reload

# Frontend (Node.js 20+)
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure

```
capstack/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # Route handlers
│   │   │   ├── health.py   # Health check endpoint
│   │   │   ├── items.py    # Example CRUD API
│   │   │   └── llm.py      # LLM endpoints + WebSocket
│   │   ├── core/           # Configuration & utilities
│   │   │   ├── config.py   # Environment settings
│   │   │   ├── database.py # SQLAlchemy setup
│   │   │   └── llm.py      # LiteLLM integration
│   │   └── db/
│   │       └── models.py   # Database models
│   └── tests/              # Pytest tests
│
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── composables/    # Vue composables (useApi, useWebSocket)
│   │   ├── pages/          # Route views
│   │   └── router/         # Vue Router config
│   └── ...
│
├── .github/workflows/      # CI/CD pipelines
├── docker-compose.yml      # One-command development
├── Makefile               # Common commands
└── .env.example           # Environment template
```

---

## 🤖 LLM Integration

CapStack uses **LiteLLM** for unified access to 100+ LLM providers.

### Configuration

Edit `.env` to set your provider:

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
OLLAMA_BASE_URL=http://localhost:11434
```

### Usage in Code

```python
from app.core.llm import llm_complete, llm_stream

# Simple completion
response = await llm_complete("Explain quantum computing")

# Streaming (for real-time UI)
async for chunk in llm_stream("Tell me a story"):
    print(chunk)
```

---

## 🛠️ Common Tasks

### Add a New API Endpoint

1. Create a file in `backend/app/api/your_endpoint.py`:

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
app.include_router(your_endpoint.router, prefix="/api")
```

### Add a New Database Model

1. Add to `backend/app/db/models.py`:

```python
class YourModel(Base):
    __tablename__ = "your_table"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
```

2. Restart the backend (tables are auto-created in dev)

### Add a New Frontend Page

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

## 📋 Make Commands

```bash
make help          # Show all commands
make dev           # Start everything (Docker)
make backend       # Start backend only
make frontend      # Start frontend only
make test          # Run tests
make lint          # Lint code
make clean         # Remove generated files
```

---

## 🔧 Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | FastAPI | Modern async Python web framework |
| | SQLAlchemy 2.0 | Async ORM with type hints |
| | LiteLLM | Unified LLM API (OpenAI, Azure, Anthropic, etc.) |
| | UV | Fast Python package manager |
| **Frontend** | Vue 3 | Progressive UI framework |
| | TypeScript | Type safety |
| | Vite | Lightning-fast build tool |
| | Tailwind CSS | Utility-first styling |
| | TanStack Query | Data fetching & caching |
| | Pinia | State management |
| **DevOps** | Docker | Containerization |
| | GitHub Actions | CI/CD pipelines |
| | Railway | Deployment platform |

---

## 🚢 Deployment

### Railway

1. Create a new project on [Railway](https://railway.app)
2. Connect your GitHub repo
3. Add environment variables from `.env.example`
4. Add `RAILWAY_TOKEN` to GitHub secrets
5. Push to `main` - auto-deploys!

### Manual Docker

```bash
# Build production images
docker compose -f docker-compose.prod.yml build

# Deploy to your server
docker compose -f docker-compose.prod.yml up -d
```

---

## 🧪 Testing

```bash
# Backend tests
cd backend && pytest -v

# With coverage
pytest --cov=app --cov-report=html
```

---

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | Environment (development/staging/production) | development |
| `DATABASE_URL` | Database connection string | sqlite (local) |
| `LITELLM_MODEL` | Default LLM model | gpt-4o-mini |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `AZURE_API_KEY` | Azure OpenAI key | - |
| `CORS_ORIGINS` | Allowed CORS origins | localhost |

See `.env.example` for all options.

---

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run `make lint` and `make test`
4. Open a PR to `main`

---

## 📄 License

MIT - Use freely for your AI innovations!

---

<p align="center">
  Built with ❤️ by the <strong>AI Product Innovation</strong> team
</p>