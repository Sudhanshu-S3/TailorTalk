FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY backend/req.txt /app/backend-requirements.txt
COPY frontend/req.txt /app/frontend-requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r backend-requirements.txt -r frontend-requirements.txt

# Copy application code
COPY backend/app /app/backend/app
COPY frontend/app.py /app/frontend/
COPY credentials.json /app/

# Set up environment variables
ENV PYTHONPATH=/app
ENV BACKEND_URL=http://localhost:8000

# Create supervisor configuration
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports (Streamlit uses 8501, FastAPI uses 8000)
EXPOSE 8000 8501

# Start supervisord as the main process
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
