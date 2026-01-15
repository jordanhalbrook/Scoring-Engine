"""
Scoring system for tracking service check results.

This module handles recording and tracking the results of service checks,
maintaining statistics and point totals per time period.
"""
from collections import defaultdict
from datetime import datetime

# Maximum number of history entries to keep (prevents memory issues)
MAX_HISTORY_SIZE = 10000

class Scorer:
    """
    Tracks scoring results for service checks per time period.
    
    Maintains:
    - total_points: Total points earned across all periods
    - current_period_points: Points earned in the current period
    - period_history: List of points earned per period
    - history: List of all service check results
    - service_stats: Per-service pass/fail statistics
    - service_period_stats: Per-service missed checks per period
    """
    def __init__(self):
        self.total_points = 0
        self.current_period_points = 0
        self.period_history = []  # List of (timestamp, points) for each period
        self.history = []
        self.service_stats = defaultdict(lambda: {"pass": 0, "fail": 0})
        # Track missed checks per service per period (requirement R2)
        self.service_period_stats = defaultdict(lambda: {"missed_checks": 0, "total_checks": 0})
        self.current_period_start = datetime.utcnow()

    def start_period(self):
        """
        Start a new scoring period.
        
        This should be called at the beginning of each time period
        before checking services. It saves the previous period's data
        and resets counters for the new period.
        """
        # Save previous period's points if any
        # (First period won't have previous data, so this is skipped)
        if self.period_history or self.current_period_points > 0:
            self.period_history.append((self.current_period_start, self.current_period_points))
        
        # Reset for new period
        self.current_period_points = 0
        self.current_period_start = datetime.utcnow()
        
        # Reset period-specific stats (but NOT missed_checks - that tracks consecutive periods)
        for service_name in self.service_period_stats:
            self.service_period_stats[service_name]["total_checks"] = 0
    
    def end_current_period(self):
        """
        Explicitly end the current period and save its data.
        
        This is for saving the final period when the engine shuts down.
        Normally, periods end automatically when start_period() is called.
        """
        if self.current_period_points > 0 or any(
            stats["total_checks"] > 0 
            for stats in self.service_period_stats.values()
        ):
            self.period_history.append((self.current_period_start, self.current_period_points))

    def record(self, result, points):
        """
        Record a service check result for the current period.
        
        Args:
            result: ServiceResult object containing check outcome
            points: Points value for this service (awarded if successful)
        """
        self.history.append(result)
        
        # Limit history size to prevent memory issues
        if len(self.history) > MAX_HISTORY_SIZE:
            self.history = self.history[-MAX_HISTORY_SIZE:]

        # Update statistics
        if result.success:
            self.total_points += points
            self.current_period_points += points
            self.service_stats[result.name]["pass"] += 1
            # Reset consecutive missed periods when service passes
            self.service_period_stats[result.name]["missed_checks"] = 0
        else:
            self.service_stats[result.name]["fail"] += 1
            # Increment consecutive missed periods counter
            # This tracks how many consecutive periods the service has been down
            self.service_period_stats[result.name]["missed_checks"] += 1
        
        # Track total checks for this service in this period
        self.service_period_stats[result.name]["total_checks"] += 1

    def get_period_summary(self):
        """
        Get summary of the current period.
        
        Returns:
            Dictionary with period statistics
        """
        return {
            "period_start": self.current_period_start,
            "period_points": self.current_period_points,
            "total_periods": len(self.period_history) + 1,
            "total_points": self.total_points
        }