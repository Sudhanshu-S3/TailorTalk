FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/code

WORKDIR /code

# Install dependencies first (better layer caching)
COPY req.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r req.txt

# Copy application code
COPY ./app ./app
COPY credentials.json /code/credentials.json

# Make sure credentials file exists (will fail the build if missing)
RUN test -f /code/credentials.json || (echo "credentials.json is missing" && false)

# Run as non-root user for better security
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /code
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Run app.main when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
