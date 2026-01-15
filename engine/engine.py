import random
import time

class ScoringEngine:
    """
    Main loop that checks services at random intervals.
    """
    def __init__(self, services, scorer, min_delay=20, max_delay=60):
        self.services = services
        self.scorer = scorer
        self.min_delay = min_delay
        self.max_delay = max_delay

    def run_once(self):
        service = random.choice(self.services)
        result = service.run_check()
        self.scorer.record(result, service.points)

    def run(self):
        while True:
            self.run_once()
            time.sleep(random.randint(self.min_delay, self.max_delay))
