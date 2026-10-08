FROM python:3.11-slim

WORKDIR /app

# System deps needed for psycopg2 (PostgreSQL driver) to compile/run
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Runs migrations, then starts the server. This means every container
# start guarantees the database schema is up to date — no manual
# "did I forget to migrate?" step.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
