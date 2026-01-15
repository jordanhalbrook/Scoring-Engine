import threading
from engine.engine import ScoringEngine
from engine.scoring import Scorer
from engine.config_loader import load_services
from web.app import create_app

services = load_services("config/services.yaml")
scorer = Scorer()
engine = ScoringEngine(services, scorer)

engine_thread = threading.Thread(target=engine.run, daemon=True)
engine_thread.start()

app = create_app(scorer)
app.run(host="0.0.0.0", port=5000)
