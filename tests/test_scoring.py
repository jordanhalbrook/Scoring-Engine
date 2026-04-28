import unittest
from datetime import datetime

from engine.scoring import MAX_HISTORY_SIZE, Scorer
from services.base import ServiceResult


def make_result(name, success, message="ok"):
    return ServiceResult(
        name=name,
        success=success,
        message=message,
        timestamp=datetime.utcnow(),
    )


class TestScorer(unittest.TestCase):
    def test_record_success_updates_points_and_stats(self):
        scorer = Scorer()
        result = make_result("web", True)

        scorer.record(result, points=10)

        self.assertEqual(scorer.total_points, 10)
        self.assertEqual(scorer.current_period_points, 10)
        self.assertEqual(scorer.service_stats["web"]["pass"], 1)
        self.assertEqual(scorer.service_stats["web"]["fail"], 0)
        self.assertEqual(scorer.service_period_stats["web"]["missed_checks"], 0)
        self.assertEqual(scorer.service_period_stats["web"]["total_checks"], 1)

    def test_record_fail_increments_missed_checks(self):
        scorer = Scorer()
        fail_result = make_result("smtp", False, "down")
        pass_result = make_result("smtp", True, "up")

        scorer.record(fail_result, points=5)
        scorer.record(fail_result, points=5)
        self.assertEqual(scorer.service_period_stats["smtp"]["missed_checks"], 2)

        scorer.record(pass_result, points=5)
        self.assertEqual(scorer.service_period_stats["smtp"]["missed_checks"], 0)

    def test_history_is_capped(self):
        scorer = Scorer()

        for idx in range(MAX_HISTORY_SIZE + 5):
            scorer.record(make_result(f"svc-{idx}", True), points=1)

        self.assertEqual(len(scorer.history), MAX_HISTORY_SIZE)
        self.assertEqual(scorer.history[0].name, "svc-5")

    def test_start_period_saves_previous_and_resets_total_checks(self):
        scorer = Scorer()
        scorer.record(make_result("dns", False), points=2)
        scorer.record(make_result("dns", True), points=2)
        previous_start = scorer.current_period_start

        scorer.start_period()

        self.assertEqual(len(scorer.period_history), 1)
        self.assertEqual(scorer.period_history[0][0], previous_start)
        self.assertEqual(scorer.period_history[0][1], 2)
        self.assertEqual(scorer.current_period_points, 0)
        self.assertEqual(scorer.service_period_stats["dns"]["total_checks"], 0)
        # Missed checks are intentionally preserved across periods.
        self.assertEqual(scorer.service_period_stats["dns"]["missed_checks"], 0)

    def test_end_current_period_appends_when_checks_ran(self):
        scorer = Scorer()
        scorer.record(make_result("ftp", False), points=1)

        scorer.end_current_period()

        self.assertEqual(len(scorer.period_history), 1)
        self.assertEqual(scorer.period_history[0][1], 0)


if __name__ == "__main__":
    unittest.main()
