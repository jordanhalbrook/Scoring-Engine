import unittest
from datetime import datetime

from engine.engine import ScoringEngine
from services.base import ServiceResult


class DummyService:
    def __init__(self, name, points, should_raise=False):
        self.name = name
        self.points = points
        self.should_raise = should_raise

    def run_check(self):
        if self.should_raise:
            raise RuntimeError("boom")
        return ServiceResult(self.name, True, "ok", datetime.utcnow())


class DummyScorer:
    def __init__(self):
        self.started = 0
        self.records = []

    def start_period(self):
        self.started += 1

    def record(self, result, points):
        self.records.append((result, points))


class TestScoringEngine(unittest.TestCase):
    def test_run_period_no_services(self):
        scorer = DummyScorer()
        engine = ScoringEngine([], scorer)

        engine.run_period()

        self.assertEqual(scorer.started, 0)
        self.assertEqual(scorer.records, [])

    def test_run_period_records_service_results(self):
        scorer = DummyScorer()
        services = [DummyService("http", 10), DummyService("smtp", 20)]
        engine = ScoringEngine(services, scorer)

        engine.run_period()

        self.assertEqual(scorer.started, 1)
        self.assertEqual(len(scorer.records), 2)
        recorded_points = sorted(points for _, points in scorer.records)
        self.assertEqual(recorded_points, [10, 20])

    def test_run_period_continues_when_single_service_fails(self):
        scorer = DummyScorer()
        services = [
            DummyService("dns", 15, should_raise=True),
            DummyService("pop3", 25),
        ]
        engine = ScoringEngine(services, scorer)

        engine.run_period()

        self.assertEqual(scorer.started, 1)
        self.assertEqual(len(scorer.records), 1)
        self.assertEqual(scorer.records[0][0].name, "pop3")
        self.assertEqual(scorer.records[0][1], 25)


if __name__ == "__main__":
    unittest.main()
