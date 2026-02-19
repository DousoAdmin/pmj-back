FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# deps del sistema (opcional, pero común)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cambia "main:app" según tu proyecto (ej: app.main:app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]