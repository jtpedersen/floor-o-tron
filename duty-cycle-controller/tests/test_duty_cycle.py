import unittest
from datetime import datetime, timedelta
from duty_cycle_controller import calculate_duty_cycle_from_history


# Helper function to create timestamps relative to a fixed "now"
def make_timestamp(now, offset):
    """
    Creates a timestamp with a given offset from a fixed base "now".

    Parameters:
    - now: The base time.
    - offset: A timedelta object representing the offset.

    Returns:
    - ISO format timestamp string.
    """
    return (now - offset).isoformat()


class TestDutyCycleCalculation(unittest.TestCase):
    def setUp(self):
        # Set up a fixed "now" for consistent testing
        self.now = datetime(2023, 10, 1, 12, 0, 0)
        self.duration = timedelta(hours=1)  # 1-hour duration for analysis

    def test_empty_history(self):
        """Test when the history is empty, the duty cycle should be 0."""
        history = []
        result = calculate_duty_cycle_from_history(history, self.duration, now=self.now)
        self.assertEqual(result, 0.0)

    def test_full_on_period(self):
        """Test when the history shows the switch was 'on' for the entire period."""
        history = [
            {
                "state": "on",
                "last_changed": make_timestamp(self.now, timedelta(hours=1)),
            },
            {"state": "on", "last_changed": make_timestamp(self.now, timedelta(0))},
        ]
        result = calculate_duty_cycle_from_history(history, self.duration, now=self.now)
        self.assertAlmostEqual(result, 1.0, places=2)

    def test_half_on_half_off(self):
        """Test when the history alternates between 'on' and 'off' evenly."""
        history = [
            {
                "state": "on",
                "last_changed": make_timestamp(self.now, timedelta(minutes=60)),
            },
            {
                "state": "off",
                "last_changed": make_timestamp(self.now, timedelta(minutes=30)),
            },
            {
                "state": "on",
                "last_changed": make_timestamp(self.now, timedelta(minutes=15)),
            },
            {"state": "off", "last_changed": make_timestamp(self.now, timedelta(0))},
        ]
        result = calculate_duty_cycle_from_history(history, self.duration, now=self.now)
        self.assertAlmostEqual(result, 0.5, places=2)

    def test_partial_on_period(self):
        """Test when the history shows 'on' for part of the period and 'off' for the rest."""
        history = [
            {
                "state": "on",
                "last_changed": make_timestamp(self.now, timedelta(minutes=45)),
            },
            {"state": "off", "last_changed": make_timestamp(self.now, timedelta(0))},
        ]
        result = calculate_duty_cycle_from_history(history, self.duration, now=self.now)
        self.assertAlmostEqual(result, 0.75, places=2)


if __name__ == "__main__":
    unittest.main()
