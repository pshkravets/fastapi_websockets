FROM python:3.12-slim

# Set working directory early
WORKDIR /app

# Copy only requirements file first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Now copy the rest of the code
COPY . .

EXPOSE 8000

# Environment variables
ENV REDIS_CHANNEL="chat"
ENV REDIS_CLIENTS_KEY="active_clients"
ENV REDIS_HOST="redis"
ENV REDIS_PORT=6379

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]