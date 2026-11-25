# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=secret,id=pip_ca \
    if [ -f /run/secrets/pip_ca ]; then export PIP_CERT=/run/secrets/pip_ca; fi; \
    pip install --no-cache-dir -r requirements.txt && useradd --uid 10001 --create-home appuser
COPY --chmod=0644 main.py core.py advanced.py intelligence.py runtime.py .
ENV PYTHONDONTWRITEBYTECODE=1
USER 10001
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
