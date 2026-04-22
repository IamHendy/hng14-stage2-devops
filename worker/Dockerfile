# ── Stage 1: Builder ──────────────────────────────────────────
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: Final image ──────────────────────────────────────
FROM python:3.11-slim-bookworm

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

RUN useradd -m appuser && chown -R appuser /app

USER appuser

# Worker has no HTTP port — healthcheck via Redis ping
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python -c "import redis, os; r=redis.Redis(host=os.getenv('REDIS_HOST','redis')); r.ping()" || exit 1

CMD ["python", "app.py"]