#!/bin/bash
export FLASK_APP=app.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=${PORT:-10000}  # Render fournit le port via $PORT
flask run
chmod +x start.sh
