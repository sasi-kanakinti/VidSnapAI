# Use Python slim
FROM python:3.11-slim

# Avoid tzdata interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project files into container
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose Railway port
ENV PORT=8080

# Start the app
CMD ["python", "main.py"]
