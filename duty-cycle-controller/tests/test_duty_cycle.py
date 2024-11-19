import unittest
from datetime import datetime, timedelta
from apps.utils import (
    calculate_duty_cycle_from_history,
    parse_iso_to_datetime,
    get_state,
)


def show_history(history, interval=1):
    """
    Displays the state history in ASCII art format between a specified time range.

    :param history: List of dictionaries with 'state' and 'last_changed' as ISO strings.
    :param begin: The start time as an int (minutes) or datetime.
    :param end: The end time as an int (minutes) or datetime.
    :param interval: The interval in minutes for each segment (default is 15 minutes).
    """

    current_time = parse_iso_to_datetime(history[0]["last_changed"])
    end = parse_iso_to_datetime(history[-1]["last_changed"])
    states = []

    while current_time <= end:
        state = get_state(history, current_time)
        states.append("*" if state == "on" else " ")
        current_time += timedelta(minutes=interval)

    # Print the ASCII representation
    print("State history:")
    print("[" + "".join(states) + "]")


class TestDutyCycleCalculation(unittest.TestCase):
    def setUp(self):
        # Set up a fixed "now" for consistent testing
        self.now = datetime.fromisoformat("2024-11-19T11:29:43.860717+00:00")
        self.duration = timedelta(hours=1)  # 1-hour duration for analysis

    def TS(self, offset=0):
        """
        Creates a timestamp with a given offset from a fixed base "now".

        Parameters:
        - now: The base time.
        - offset: A timedelta object representing the offset.

        Returns:
        - ISO format timestamp string.
        """
        if not isinstance(offset, timedelta):
            offset = timedelta(minutes=offset)
        return (self.now - offset).isoformat()

    def test_empty_history(self):
        """Test when the history is empty, the duty cycle should be 0."""
        history = []
        result = calculate_duty_cycle_from_history(history, self.TS())
        self.assertEqual(result, 0.0)

    def test_full_on_period(self):
        """Test when the history shows the switch was 'on' for the entire period."""
        history = [
            {
                "state": "on",
                "last_changed": self.TS(timedelta(hours=1)),
            },
            {"state": "on", "last_changed": self.TS(timedelta(0))},
        ]
        result = calculate_duty_cycle_from_history(history, self.TS())
        self.assertAlmostEqual(result, 1.0, places=2)

    def test_half_on_half_off(self):
        """Test when the history alternates between 'on' and 'off' evenly."""
        history = [
            {
                "state": "on",
                "last_changed": self.TS(timedelta(minutes=60)),
            },
            {
                "state": "off",
                "last_changed": self.TS(timedelta(minutes=30)),
            },
            {
                "state": "on",
                "last_changed": self.TS(timedelta(minutes=15)),
            },
            {"state": "off", "last_changed": self.TS(timedelta(0))},
        ]
        result = calculate_duty_cycle_from_history(history, self.TS())
        self.assertAlmostEqual(result, 0.75, places=2)

    def test_partial_on_period(self):
        """Test when the history shows 'on' for part of the period and 'off' for the rest."""
        history = [
            {
                "state": "on",
                "last_changed": self.TS(timedelta(minutes=45)),
            },
            {"state": "off", "last_changed": self.TS(timedelta(0))},
        ]
        result = calculate_duty_cycle_from_history(history, self.TS())
        self.assertAlmostEqual(result, 1.0, places=2)

    def test_with_real_data(self):
        """got some data"""
        history = [
            {
                "entity_id": "input_boolean.fakeheater",
                "state": "on",
                "attributes": {"icon": "mdi:radiator", "friendly_name": "FakeHeater"},
                "last_changed": "2024-11-19T10:57:25+00:00",
                "last_updated": "2024-11-19T10:57:25+00:00",
            },
            {
                "entity_id": "input_boolean.fakeheater",
                "state": "on",
                "attributes": {"icon": "mdi:radiator", "friendly_name": "FakeHeater"},
                "last_changed": "2024-11-19T11:05:05.449374+00:00",
                "last_updated": "2024-11-19T11:05:05.449374+00:00",
            },
            {
                "entity_id": "input_boolean.fakeheater",
                "state": "on",
                "attributes": {"icon": "mdi:radiator", "friendly_name": "FakeHeater"},
                "last_changed": "2024-11-19T11:14:25.893997+00:00",
                "last_updated": "2024-11-19T11:14:25.893997+00:00",
            },
            {
                "entity_id": "input_boolean.fakeheater",
                "state": "on",
                "attributes": {"icon": "mdi:radiator", "friendly_name": "FakeHeater"},
                "last_changed": "2024-11-19T11:17:08.632652+00:00",
                "last_updated": "2024-11-19T11:17:08.632652+00:00",
            },
            {
                "entity_id": "input_boolean.fakeheater",
                "state": "on",
                "attributes": {"icon": "mdi:radiator", "friendly_name": "FakeHeater"},
                "last_changed": "2024-11-19T11:28:43.860717+00:00",
                "last_updated": "2024-11-19T11:28:43.860717+00:00",
            },
        ]

        result = calculate_duty_cycle_from_history(
            history, datetime.fromisoformat("2024-11-19T11:29:43.860717+00:00")
        )
        self.assertAlmostEqual(result, 1.0)


if __name__ == "__main__":
    unittest.main()
