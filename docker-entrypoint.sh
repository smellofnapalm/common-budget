#!/bin/sh
set -e

echo "Initializing database (create types/tables)..."
python -c "from initialize_tables import initialize; initialize()"

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 main:app
