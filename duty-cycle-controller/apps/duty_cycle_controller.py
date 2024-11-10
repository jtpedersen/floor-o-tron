import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timedelta
import re
from datetime import timedelta


def parse_time_literal(time_str):
    """Parses a time string like '1H', '1_hour', '15 minutes' into a timedelta object."""
    time_units = {
        "s": "seconds",
        "sec": "seconds",
        "second": "seconds",
        "seconds": "seconds",
        "m": "minutes",
        "min": "minutes",
        "minute": "minutes",
        "minutes": "minutes",
        "h": "hours",
        "hour": "hours",
        "hours": "hours",
        "d": "days",
        "day": "days",
        "days": "days",
    }

    # Regex to match various time formats like '1H', '1_hour', '15 minutes'
    match = re.match(r"(\d+)\s*([a-zA-Z_]+)", time_str)
    if not match:
        raise ValueError(f"Invalid time format: {time_str}")

    value, unit = match.groups()
    unit = unit.lower().replace("_", "")

    if unit not in time_units:
        raise ValueError(f"Unsupported time unit: {unit}")

    # Create a timedelta object with the appropriate keyword argument
    return timedelta(**{time_units[unit]: int(value)})


class DutyCycleController(hass.Hass):
    def initialize(self):

        self.heater_switch = self.args.get("heater_switch")
        if not isinstance(self.heater_switch, list):
            self.heater_switch = [heater_switch]
        self.duty_cycle_percentage = 0.5
        self.min_pulse_width = parse_time_literal(
            self.args.get("min_pulse_width", "15 minutes")
        )
        self.duration = parse_time_literal(self.args.get("duration", "1 hour"))
        self.cycle_time = parse_time_literal(self.args.get("cycle_time", "1 day"))

        # Track on/off history
        self.history = []

        # Schedule the duty cycle check loop
        self.run_every(self.duty_cycle_check, "now", self.adjustment_interval)

    def calc_duty_cycle(self):
        """Calculate the current duty cycle based on the history."""
        now = datetime.now()

        # Clean history older than history_duration to manage memory usage
        self.history = [
            entry
            for entry in self.history
            if entry["timestamp"] > now - timedelta(seconds=self.history_duration)
        ]

        # Calculate total on-time
        on_time = sum(
            entry["duration"] for entry in self.history if entry["state"] == "on"
        )
        total_time = self.history_duration

        return on_time / total_time if total_time > 0 else 0

    def set_state(self, switch, state):
        current_state = self.get_state(switch)
        if current_state != state:
            if state == "on":
                self.call_service("switch/turn_on", entity_id=switch)
            elif state == "off":
                self.call_service("switch/turn_off", entity_id=switch)

            # Record state change
            self.record_state(switch, state)

    def turn_on(self):
        for switch in self.heater_switch:
            self.set_state(switch, "on")

    def turn_off(self):
        for switch in self.heater_switch:
            self.set_state(switch, "off")

    def duty_cycle_check(self, kwargs):
        """Check the current duty cycle and adjust switch states accordingly."""
        current_duty_cycle = self.calc_duty_cycle()

        # Compare and adjust each heater switch
        if current_duty_cycle > self.duty_cycle_percentage:
            self.turn_off()
            self.log(
                f"Duty cycle exceeded: {current_duty_cycle:.2%}. Turning off heat."
            )
        else:
            self.turn_on()
            self.log(
                f"Duty cycle below target: {current_duty_cycle:.2%}. Turning on heat."
            )
