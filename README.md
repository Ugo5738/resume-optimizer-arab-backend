# Resume Optimizer Arab Backend

AI-powered resume optimization service with multi-language support (English & Arabic).

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)

## Features

- **AI-Powered Optimization** - Uses LLMs to analyze resumes against job descriptions
- **Multi-Language Support** - English and Arabic with translation capabilities
- **Multiple LLM Providers** - OpenAI GPT-4o, Google Gemini, Anthropic Claude
- **Document Parsing** - Extract text from PDF, DOCX, and images (OCR)
- **Alignment Analysis** - Identifies matched, missing, and weak keywords
- **Score & Recommendations** - Match score (0-100) with actionable suggestions
- **Microservices Architecture** - Scalable, containerized services

## Architecture

```
┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│                 │     │                     │     │                 │
│  Frontend App   │────▶│   Gateway Service   │────▶│  Parser Service │
│                 │     │     (Port 8000)     │     │   (Port 8002)   │
└─────────────────┘     └──────────┬──────────┘     └─────────────────┘
                                   │                 PDF/DOCX/OCR
                                   ▼
                        ┌─────────────────────┐
                        │                     │
                        │ Orchestrator Service│────▶ LLM Provider
                        │    (Port 8001)      │     (OpenAI/Gemini/Claude)
                        │                     │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │                     │
                        │  PostgreSQL (Supabase)│
                        │                     │
                        └─────────────────────┘
```

### Services

| Service | Port | Description |
|---------|------|-------------|
| **Gateway** | 8000 | API entry point, authentication, request routing |
| **Orchestrator** | 8001 | Job management, task queue, background worker |
| **Parser** | 8002 | Document text extraction (PDF, DOCX, OCR) |

## Tech Stack

- **Framework**: FastAPI + Uvicorn
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Auth**: JWT (Supabase)
- **LLM**: OpenAI / Google Gemini / Anthropic Claude
- **Document Parsing**: PyMuPDF, python-docx, EasyOCR
- **Caching**: Redis
- **Containerization**: Docker Compose

## Project Structure

```
resume-optimizer-arab-backend/
├── libs/                           # Shared libraries
│   ├── ai/                        # LLM provider abstractions
│   │   ├── base.py               # Base provider interface
│   │   ├── openai_provider.py    # OpenAI implementation
│   │   ├── gemini_provider.py    # Google Gemini implementation
│   │   ├── anthropic_provider.py # Anthropic Claude implementation
│   │   └── factory.py            # Provider factory
│   ├── auth/                      # JWT authentication
│   ├── common/                    # Config, logging, utilities
│   └── db/                        # Database setup, base models
├── services/
│   ├── gateway_service/           # API Gateway
│   │   └── app/
│   │       ├── main.py
│   │       └── routers/
│   ├── orchestrator_service/      # Job orchestration & worker
│   │   └── app/
│   │       ├── main.py
│   │       ├── worker.py         # Background task processor
│   │       ├── core/             # Business logic
│   │       │   └── optimizer.py  # Resume optimization
│   │       ├── db/               # Models & repository
│   │       └── routers/
│   └── parser_service/            # Document parsing
│       └── app/
├── scripts/
│   └── db_manage.py              # Database management CLI
├── docker-compose.yml
├── pyproject.toml
└── .env.dev                       # Environment configuration
```

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Supabase account (for PostgreSQL)
- LLM API key (one of: OpenAI, Google Gemini, or Anthropic)

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd resume-optimizer-arab-backend
```

### 2. Configure environment

```bash
# Copy example env file
cp .env.dev.example .env.dev

# Edit with your credentials
vim .env.dev
```

### 3. Set up database

```bash
# Install dependencies locally (for running migrations)
pip install -e .

# Create tables and run migrations
python scripts/db_manage.py fresh -m "initial_schema"
```

### 4. Start services

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f
```

### 5. Verify

```bash
# Check health
curl http://localhost:8000/health
# Expected: {"status":"ok","service":"gateway"}
```

## Environment Variables

Create a `.env.dev` file with the following variables:

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg://user:pass@host:5432/db` |
| `SUPABASE_URL` | Supabase project URL | `https://xxx.supabase.co` |
| `SUPABASE_SERVICE_KEY` | Supabase service role key | `eyJ...` |
| `SUPABASE_JWT_SECRET` | JWT signing secret | `your-jwt-secret` |
| `LLM_PROVIDER` | LLM to use: `openai`, `gemini`, or `anthropic` | `openai` |

### LLM API Keys (at least one required)

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key (for GPT-4o) |
| `GEMINI_API_KEY` | Google AI API key (for Gemini) |
| `ANTHROPIC_API_KEY` | Anthropic API key (for Claude) |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Environment mode |
| `LOG_LEVEL` | `INFO` | Logging level |
| `POLL_INTERVAL` | `2` | Worker poll interval (seconds) |
| `FRONTEND_URL` | `http://localhost:3000` | Frontend URL for CORS |

### Example `.env.dev`

```bash
# Supabase
SUPABASE_URL=https://yourproject.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_JWT_SECRET=your-jwt-secret
DATABASE_URL=postgresql+psycopg://postgres.xxx:password@aws-0-region.pooler.supabase.com:6543/postgres

# LLM Provider
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...

# Or use Gemini
# LLM_PROVIDER=gemini
# GEMINI_API_KEY=AIza...

# Or use Anthropic
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-...
```

## Database Management

The `scripts/db_manage.py` CLI provides idempotent database operations:

```bash
# Show current migration status
python scripts/db_manage.py status

# Run pending migrations
python scripts/db_manage.py migrate

# Generate new migration from model changes
python scripts/db_manage.py generate -m "add_new_field"

# Full reset: drop everything, generate migration, apply
python scripts/db_manage.py fresh -m "initial_schema"

# Drop all tables and enums (destructive!)
python scripts/db_manage.py nuke
```

## API Reference

All endpoints require authentication via Bearer token (Supabase JWT).

### Jobs

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/jobs` | Create optimization job |
| `GET` | `/jobs` | List user's jobs |
| `GET` | `/jobs/{id}` | Get job with optimization result |
| `POST` | `/jobs/{id}/refine` | Refine completed job with new instructions |

### Resumes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/resumes/upload` | Upload resume file for text extraction |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |

## API Usage Examples

### Create an Optimization Job

```bash
curl -X POST http://localhost:8000/jobs \
  -H "Authorization: Bearer $SUPABASE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resumeText": "John Doe\nSoftware Engineer\n\nSkills: Python, FastAPI, PostgreSQL",
    "jobDescription": "Looking for Python developer with FastAPI experience...",
    "resumeLang": "en",
    "jdLang": "en"
  }'
```

**Response:**
```json
{
  "data": {
    "job": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "userId": "user-uuid",
      "status": "queued",
      "createdAt": "2024-01-15T10:30:00Z"
    }
  },
  "error": null
}
```

### Get Job Result

```bash
curl http://localhost:8000/jobs/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer $SUPABASE_TOKEN"
```

**Response (when complete):**
```json
{
  "data": {
    "job": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "complete",
      "result": {
        "score": 85,
        "missingKeywords": ["Docker", "Kubernetes"],
        "coveredKeywords": ["Python", "FastAPI", "PostgreSQL"],
        "changeLog": [
          "Add Docker experience to match job requirements",
          "Consider adding Kubernetes knowledge"
        ],
        "previewMarkdown": "# John Doe\n\n**Software Engineer**\n\n## Skills\n- Python\n- FastAPI\n...",
        "extractedEntities": {
          "skills": ["Python", "FastAPI", "PostgreSQL"],
          "experience": [...]
        },
        "alignmentInsights": {
          "matched": ["Python", "FastAPI"],
          "missing": ["Docker", "Kubernetes"],
          "weak": []
        }
      }
    }
  },
  "error": null
}
```

### Upload Resume for Text Extraction

```bash
curl -X POST http://localhost:8000/resumes/upload \
  -H "Authorization: Bearer $SUPABASE_TOKEN" \
  -F "file=@resume.pdf"
```

## LLM Providers

Switch between providers by setting `LLM_PROVIDER` in your environment:

| Provider | Value | Model | Notes |
|----------|-------|-------|-------|
| OpenAI | `openai` | GPT-4o | Best overall quality |
| Google Gemini | `gemini` | Gemini 2.0 Flash | Fast, good multilingual |
| Anthropic | `anthropic` | Claude Sonnet | Excellent reasoning |

```bash
# In .env.dev
LLM_PROVIDER=openai    # Use OpenAI
LLM_PROVIDER=gemini    # Use Google Gemini
LLM_PROVIDER=anthropic # Use Anthropic Claude
```

## Docker Commands

```bash
# Start all services in background
docker compose up -d

# View logs (all services)
docker compose logs -f

# View logs (specific service)
docker compose logs -f orchestrator-service

# Restart services (after code changes)
docker compose restart

# Rebuild and restart (after dependency changes)
docker compose up -d --build

# Stop all services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v
```

## Development

### Running Locally (without Docker)

```bash
# Install dependencies
pip install -e ".[dev]"

# Start each service in separate terminals
uvicorn services.gateway_service.app.main:app --port 8000 --reload
uvicorn services.orchestrator_service.app.main:app --port 8001 --reload
uvicorn services.parser_service.app.main:app --port 8002 --reload
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov=libs

# Run specific test file
pytest tests/test_optimizer.py -v
```

### Code Formatting

```bash
# Format code with ruff
ruff format .

# Check linting
ruff check .

# Fix auto-fixable issues
ruff check . --fix
```

## Troubleshooting

### "relation task_queue does not exist"

Database tables not created. Run:
```bash
python scripts/db_manage.py fresh
```

### "429 RESOURCE_EXHAUSTED" (Gemini)

Gemini free tier quota exceeded. Either:
- Wait for quota reset (daily)
- Switch to OpenAI: `LLM_PROVIDER=openai`
- Enable billing on Google Cloud

### "insufficient_quota" (OpenAI)

OpenAI credits exhausted. Add billing at https://platform.openai.com/settings/organization/billing

### Services not connecting

Check service URLs in environment:
```bash
# For Docker
ORCHESTRATOR_SERVICE_URL=http://orchestrator-service:8001
PARSER_SERVICE_URL=http://parser-service:8002

# For local development
ORCHESTRATOR_SERVICE_URL=http://localhost:8001
PARSER_SERVICE_URL=http://localhost:8002
```

## License

MIT License - see LICENSE file for details.
