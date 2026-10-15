
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY mcp_server/ ./mcp_server/
COPY knowledge_base/ ./knowledge_base/
COPY data/ ./data/

EXPOSE 8000 8001
