#!/usr/bin/env bash

echo "Rss parser is running.."

export PYTHON_PATH=/app

uvicorn main:app  --host 0.0.0.0 --port ${SERVICE_PORT}