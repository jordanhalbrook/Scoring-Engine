"""
Main scoring engine that performs service checks.

This module runs the main loop that periodically checks services
and records the results in the scorer.
"""
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class ScoringEngine:
    """
    Main loop that checks all services concurrently at regular intervals.
    """
    def __init__(self, services, scorer, check_interval=60):
        """
        Initialize the scoring engine.
        
        Args:
            services: List of service check objects
            scorer: Scorer instance to record results
            check_interval: Seconds between checking all services (default: 60)
        """
        self.services = services
        self.scorer = scorer
        self.check_interval = check_interval

    def check_service(self, service):
        """
        Check a single service and return the result.
        
        This method is designed to be called concurrently.
        
        Args:
            service: ServiceCheck object to test
            
        Returns:
            Tuple of (service, result) for recording
        """
        result = service.run_check()
        return (service, result)

    def run_period(self):
        """
        Check all services concurrently in one time period.

        """
        if not self.services:
            return
        
        # Start a new scoring period
        self.scorer.start_period()
        
        # Use ThreadPoolExecutor to check all services concurrently
        with ThreadPoolExecutor(max_workers=len(self.services)) as executor:
            # Submit all service checks
            future_to_service = {
                executor.submit(self.check_service, service): service
                for service in self.services
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_service):
                try:
                    service, result = future.result()
                    self.scorer.record(result, service.points)
                except Exception as e:
                    # If a check itself fails (not the service), log it
                    service = future_to_service[future]
                    print(f"Error checking {service.name}: {e}")

    def run(self):
        """
        Main loop that runs continuously, checking all services
        concurrently at regular intervals.
        """
        while True:
            self.run_period()
            time.sleep(self.check_interval)
