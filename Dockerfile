FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
COPY scripts/sanitize_requirements.py /tmp/sanitize_requirements.py

RUN python /tmp/sanitize_requirements.py /tmp/requirements.txt /tmp/requirements-runtime.txt
RUN python -m pip install --upgrade pip && python -m pip install -r /tmp/requirements-runtime.txt

COPY . /app

FROM base AS backend
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS frontend
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
