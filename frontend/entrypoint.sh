#!/bin/bash
set -e

# Railway provides PORT environment variable
PORT=${PORT:-8501}

echo "Starting Streamlit server on port $PORT..."

exec streamlit run main.py \
  --server.port=$PORT \
  --server.address=0.0.0.0 \
  --server.headless=true
