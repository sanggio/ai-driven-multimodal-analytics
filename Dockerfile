FROM python:3.12-slim as builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY app ./app
COPY env.example .env.example

RUN useradd -m -u 1000 appuser && \
    cp -r /root/.local /home/appuser/.local && \
    chown -R appuser:appuser /app /home/appuser/.local

ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

