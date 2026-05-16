#!/bin/bash
set -e

# Railway provides PORT environment variable
PORT=${PORT:-8000}

# Run migrations/init if needed
echo "Starting FastAPI server on port $PORT..."

exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
