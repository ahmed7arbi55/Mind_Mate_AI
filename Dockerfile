# Build stage - Use pytorch official slim image
FROM pytorch/pytorch:2.1.0-runtime-slim as builder

WORKDIR /build

# Install only necessary build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies to user directory
COPY requirements.txt .
RUN pip install --no-cache-dir --user \
    ultralytics \
    opencv-python \
    numpy \
    matplotlib \
    fastapi==0.109.0 \
    uvicorn==0.27.0 \
    httpx==0.26.0 \
    pydantic==2.5.3 \
    python-multipart==0.0.6 \
    pillow && \
    find /root/.local -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Final runtime stage - Use pytorch slim image
FROM pytorch/pytorch:2.1.0-runtime-slim

WORKDIR /app

# Install only runtime dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled Python packages from builder
COPY --from=builder /root/.local /root/.local

# Set PATH and environment
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy only necessary application files (model files will be downloaded at runtime)
COPY app/ ./app/
COPY run.py .
COPY requirements.txt .

# Create directory for downloaded models
RUN mkdir -p /app/models

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]
