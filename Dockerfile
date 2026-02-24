FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

# Copy project files
COPY . .

# Build frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# Setup backend
WORKDIR /app/backend

# Create necessary directories
RUN mkdir -p model uploads database logs

# Expose ports
EXPOSE 5000 3000

# Start both services
CMD ["sh", "-c", "python app.py & cd /app/frontend && PORT=3000 npm start"]
