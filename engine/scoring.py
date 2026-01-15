class Scorer:
    def __init__(self):
        self.total_points = 0
        self.history = []

    def record(self, result, points):
        self.history.append(result)
        if result.success:
            self.total_points += points
