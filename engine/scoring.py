"""
Scoring system for tracking service check results.

This module handles recording and tracking the results of service checks,
maintaining statistics and point totals.
"""
from collections import defaultdict

# Maximum number of history entries to keep (prevents memory issues)
MAX_HISTORY_SIZE = 10000

class Scorer:
    """
    Tracks scoring results for service checks.
    
    Maintains:
    - total_points: Cumulative points earned (only increases)
    - history: List of all service check results
    - service_stats: Per-service pass/fail statistics
    """
    def __init__(self):
        self.total_points = 0
        self.history = []
        self.service_stats = defaultdict(lambda: {"pass": 0, "fail": 0})

    def record(self, result, points):
        """
        Record a service check result.
        
        Args:
            result: ServiceResult object containing check outcome
            points: Points value for this service (awarded if successful)
        """
        self.history.append(result)
        
        # Limit history size to prevent memory issues
        if len(self.history) > MAX_HISTORY_SIZE:
            self.history = self.history[-MAX_HISTORY_SIZE:]

        if result.success:
            self.total_points += points
            self.service_stats[result.name]["pass"] += 1
        else:
            self.service_stats[result.name]["fail"] += 1
