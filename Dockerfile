FROM python:3.10-slim

# --- System dependencies ---
RUN apt-get update && \
    apt-get install -y git curl gnupg build-essential ninja-build && \
    curl -fsSL https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor -o /etc/apt/trusted.gpg.d/adoptium.gpg && \
    echo "deb https://packages.adoptium.net/artifactory/deb bookworm main" | tee /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && \
    apt-get install -y temurin-21-jre && \
    rm -rf /var/lib/apt/lists/*

# --- Set up working directory and env ---
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/keats-search-eval/src

# --- Install Python packages ---
COPY requirements.txt .
RUN pip install --upgrade pip

# Install torch and faiss
RUN pip install torch==2.7.1 torchvision==0.22.1 torchaudio==2.7.1
RUN pip install faiss-cpu==1.11.0

# Install core requirements
RUN pip install -r requirements.txt

# Install ColBERT from source (CPU-safe build)
RUN git clone https://github.com/stanford-futuredata/ColBERT.git /tmp/colbert && \
    cd /tmp/colbert && \
    pip install .

# Install SPLADE from GitHub
RUN pip install git+https://github.com/naver/splade.git

# Upgrade transformers to latest if needed
RUN pip install --upgrade transformers

# --- Final workdir ---
WORKDIR /app/keats-search-eval
