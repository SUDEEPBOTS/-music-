FROM python:3.10-bullseye

# NodeJS install (latest)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_19.x | bash - && \
    apt-get install -y nodejs && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Work directory
WORKDIR /app

# Copy files
COPY . .

# Install Python deps
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Start bot
CMD ["bash", "start"]
