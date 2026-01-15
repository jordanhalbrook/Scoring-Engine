"""
Main scoring engine that performs service checks.

This module runs the main loop that periodically checks services
and records the results in the scorer.
"""
import random
import time

class ScoringEngine:
    """
    Main loop that checks services at random intervals.
    """
    def __init__(self, services, scorer, min_delay=20, max_delay=60):
        """
        Initialize the scoring engine.
        
        Args:
            services: List of service check objects
            scorer: Scorer instance to record results
            min_delay: Minimum seconds between checks (default: 20)
            max_delay: Maximum seconds between checks (default: 60)
        """
        self.services = services
        self.scorer = scorer
        self.min_delay = min_delay
        self.max_delay = max_delay

    def run_once(self):
        service = random.choice(self.services)
        result = service.run_check()
        self.scorer.record(result, service.points)

    def run(self):
        """
        Main loop that runs continuously, checking services at random intervals.
        """
        while True:
            self.run_once()
            time.sleep(random.randint(self.min_delay, self.max_delay))
