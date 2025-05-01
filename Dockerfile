FROM python:3.12-slim-buster

RUN pip install --upgrade pip && pip install -r /app/requirements.txt
WORKDIR /app

COPY . .

EXPOSE 8000

ENV REDIS_CHANNEL="chat"
ENV REDIS_CLIENTS_KEY="active_clients"
ENV REDIS_HOST="redis"
ENV REDIS_PORT=6379

CMD ["uvicorn", "main:app", "--port", "8000", "--workers", "2"]

