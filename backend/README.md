# Backend - Social Media AI Platform

Quick start for local development (backend).

Prerequisites
- Python 3.11
- Docker & Docker Compose (for containerized run)

Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
```

Run migrations

```bash
alembic upgrade head
```

Run locally

```bash
# dev
uvicorn app.main:app --reload
```

Run with Docker Compose

```bash
docker compose up --build
```

Swagger UI: http://127.0.0.1:8000/docs

Endpoints to verify (Swagger):

- `POST /api/v1/auth/register` — register a user
- `POST /api/v1/auth/login` — login to receive JWT
- Click **Authorize** and paste `Bearer <token>`
- `GET /api/v1/auth/me` — returns current user