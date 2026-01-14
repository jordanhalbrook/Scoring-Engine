import random
import time

class ScoringEngine:
    def __init__(self, services, scorer):
        self.services = services
        self.scorer = scorer

    def run(self):
        while True:
            service = random.choice(self.services)
            result = service.run_check()
            self.scorer.record(result, service.points)
            time.sleep(random.randint(20, 60))
