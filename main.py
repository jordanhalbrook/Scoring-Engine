"""
Main entry point for the Scoring Engine.

Starts the scoring engine in a background thread and runs the web interface.
"""
import threading
from engine.engine import ScoringEngine
from engine.scoring import Scorer
from engine.config_loader import load_services
from web.app import create_app

# Load services from configuration
services = load_services("config/services.yaml")

# Create scorer and engine
# Check interval: 60 seconds (checks all services every 60 seconds)
scorer = Scorer()
engine = ScoringEngine(services, scorer, check_interval=60)

# Start the scoring engine in a background thread
engine_thread = threading.Thread(target=engine.run, daemon=True)
engine_thread.start()

# Start the web interface
app = create_app(scorer)

# For development: use Flask's built-in server
# For production: use gunicorn (see DEPLOYMENT.md)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
