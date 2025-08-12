# Small, reproducible image for Render worker
FROM python:3.12-slim

# Prevents Python from buffering logs (we want immediate logs in Render)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (only what's needed for requests & SSL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root for safety
RUN useradd -ms /bin/bash appuser
USER appuser

# Start as a worker (no port exposed)
CMD ["python", "main.py"]
