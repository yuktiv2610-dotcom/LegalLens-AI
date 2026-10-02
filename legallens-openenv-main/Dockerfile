FROM python:3.11-slim

# Create a non-root user to run the app (Required for Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Switch to root temporarily to install system dependencies
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files with correct ownership
COPY --chown=user . .

# Build frontend
RUN if [ -f "frontend/package.json" ]; then \
    cd frontend && npm ci && npm run build; \
    fi

# Switch back to the non-root user
USER user

# Expose the port required by Hugging Face Spaces
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Start the FastAPI server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
