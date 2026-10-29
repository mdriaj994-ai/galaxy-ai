FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create data directory for SQLite
RUN mkdir -p data audio

# Expose port
EXPOSE 5000

# Environment
ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=1

# Start server
CMD ["python", "server.py"]

