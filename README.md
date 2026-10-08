# Vigil

**An adaptive, self-monitoring, multi-channel threat detection platform.**

Vigil analyzes email content, SMS text, and URLs/websites to detect phishing,
scams, and fraudulent activity — including fake e-commerce sites. It produces
an explainable verdict (threat type, confidence, plain-language reasoning),
monitors its own accuracy over time, and is stress-tested against
adversarially reworded attacks.

Design decisions log: [`docs/DECISIONS.md`](docs/DECISIONS.md)

## Project Status

🚧 Foundation complete — layered backend with working authentication, database
migrations, and CI. Core detection engine (Month 1) not yet implemented.

## Architecture (high level)

```
User Input → NLP → Threat Intelligence → Sender Verification
→ Evidence Fusion → Explainable Decision → Dashboard
→ Monitoring → Drift Detection → Adversarial Evaluation → Retraining
```

The Coordinator that routes between stages is a **deterministic decision
policy**, not an autonomous agent. The LLM's only role is generating the
final human-readable explanation from structured evidence.

## Backend Architecture

```
backend/app/
├── core/       # settings, security (password hashing, JWT)
├── db/         # database engine/session management
├── models/     # SQLAlchemy ORM models (database shape)
├── schemas/    # Pydantic schemas (API request/response shape)
├── api/v1/     # versioned routes
│   └── endpoints/
├── services/   # business logic (NLP, Coordinator, evidence fusion — Month 1+)
└── main.py     # thin entrypoint, wires everything together
```

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI (Python) |
| Auth | JWT (python-jose) + bcrypt password hashing, role-based (analyst/admin) |
| Database | PostgreSQL (SQLite for quick local dev) |
| Migrations | Alembic |
| Frontend | React, TypeScript, Tailwind CSS |
| Content model | DistilBERT (Hugging Face) |
| Explanation LLM | Groq / Gemini free tier |
| Cache | Redis |
| Threat intel | VirusTotal, PhishTank, OpenPhish |
| Model tracking | MLflow |
| Drift monitoring | Evidently AI |
| LLM observability | Langfuse |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Deployment | Azure for Students |

## Running Locally (no Docker)

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head           # creates vigil_dev.db with the users table
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` — Hello World JSON response.
Interactive API docs: `http://localhost:8000/docs`

Try the auth flow directly from `/docs`: register a user via
`POST /api/v1/auth/register`, then log in via `POST /api/v1/auth/login`
to get a token, then click "Authorize" in the docs UI and paste it in to
call `GET /api/v1/auth/me`.

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

## Running with Docker (full stack: API + Postgres + Redis)

```bash
docker compose up --build
```

## Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```
