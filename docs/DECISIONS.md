# Design Decisions Log

A running record of significant design/architecture decisions, why they were
made, and what alternatives were considered.

---

## Coordinator is a deterministic decision policy, not an autonomous agent

**Decision:** The Coordinator that routes between analysis stages uses fixed,
rule-based branching logic. The LLM is restricted to exactly two roles:
generating the final human-readable explanation from structured evidence,
and generating adversarial test variants for robustness evaluation.

**Why:** Reliability, auditability, and viva defensibility — every decision
traces to an explicit rule, not opaque model reasoning.

---

## Backend framework: FastAPI

**Decision:** FastAPI over Flask/Django.

**Why:** Async support for concurrent external API calls, automatic
OpenAPI docs, strong typing via Pydantic.

---

## Layered backend architecture: core / db / models / schemas / api / services

**Decision:** Separate SQLAlchemy ORM models (`app/models/`) from Pydantic
API schemas (`app/schemas/`), and separate route handlers (`app/api/`) from
business logic (`app/services/`).

**Alternatives considered:** A flatter structure with everything in one or
two files, common in small/tutorial projects.

**Why:** This is standard practice in production backend codebases — it
keeps the database shape and the API shape independently changeable (e.g. a
password hash must exist in the DB model but must never appear in an API
response), and keeps business logic unit-testable without needing to spin
up HTTP requests. Worth the small extra setup cost for the "I know how real
backend teams structure code" signal alone.

---

## Versioned API (`/api/v1/`)

**Decision:** All routes are mounted under `/api/v1/`, not a bare `/api/`.

**Why:** If the API ever needs a breaking change later, `/api/v2/` can be
added alongside `/api/v1/` without breaking anything already depending on
v1. Costs nothing now, signals real API design discipline.

---

## Real authentication: JWT + role-based access (analyst / admin)

**Decision:** Proper password hashing (bcrypt via passlib) and JWT-based
login, with two roles: `analyst` (submits analyses, sees own history) and
`admin` (also sees the Monitoring/MLOps dashboard).

**Alternatives considered:** No-login single-user demo.

**Why:** A role split makes the dashboard genuinely behave differently per
user type, which is a stronger "enterprise" story than a flat app where
everyone sees everything. This was an explicit scope decision, not a
default — single-user would have been faster to build.

---

## Database migrations via Alembic

**Decision:** Every schema change goes through an Alembic migration script,
never a manual/hand-edited database change.

**Why:** Migrations are reviewable, reversible, and reproducible across
environments (local SQLite for quick dev, Postgres in Docker/production).
This is standard practice on any real backend team and is a meaningful gap
in most student projects, which usually just hand-edit a dev database.

---

## SQLite for quick local dev, Postgres via Docker Compose for "real" runs

**Decision:** `DATABASE_URL` defaults to local SQLite so the app boots with
zero setup, but `docker compose up` automatically runs against a real
Postgres container instead.

**Why:** Fast iteration locally without sacrificing an accurate,
production-like environment when it matters (Docker Compose, CI, and the
actual Azure deployment all use Postgres).

---

## Project structure: monorepo (backend + frontend in one repo)

**Decision:** Single repository containing both `backend/` and `frontend/`.

**Why:** Solo development, simpler to manage, version, and deploy together
via one Docker Compose setup and one CI/CD pipeline.

---

## Template for future entries

```
## <short decision title>

**Decision:** <what was decided>

**Alternatives considered:** <what else was considered>

**Why this choice:** <the reasoning>
```
