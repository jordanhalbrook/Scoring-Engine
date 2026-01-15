from collections import defaultdict

class Scorer:
    def __init__(self):
        self.total_points = 0
        self.history = []
        self.service_status =defaultdict(lambda: {"pass": 0, "fail": 0})

    def record(self, result, points):
        self.history.append(result)

        if result.success:
            self.total_points += points
            self.service_stats[result.name]["pass"] += 1
        else:
            self.service_stats[result.name]["fail"] += 1
