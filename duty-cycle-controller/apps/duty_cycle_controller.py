import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timedelta
import re
import utils


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

        heater_switch = self.args.get("heater_switch")
        if not isinstance(heater_switch, list):
            heater_switch = [heater_switch]
        self.duty_cycle_percentage = 0.5
        self.min_pulse_width = parse_time_literal(
            self.args.get("min_pulse_width", "15 minutes")
        )
        self.history_duration = parse_time_literal(self.args.get("duration", "1 hour"))
        self.adjustment_interval = parse_time_literal(
            self.args.get("adjustment_interval", "30 seconds")
        )

        self.heater_switch = [self.get_entity(e) for e in heater_switch]
        for e in self.heater_switch:
            assert e.exists()

        # Track on/off history
        self.history = []

        # Schedule the duty cycle check loop
        self.run_every(
            self.duty_cycle_check,
            "now",
            interval=self.adjustment_interval.total_seconds(),
        )

    def set_heater_state(self, switch, state):
        current_state = switch.get_state()
        if current_state != state:
            if state == "on":
                switch.turn_on()
            elif state == "off":
                switch.turn_off()

            # Record state change
            self.record_state(switch, state)

    def record_state(self, switch, state):
        """Record the current state of a switch with a timestamp."""
        now = datetime.now()
        self.history.append(
            {
                "timestamp": now,
                "state": state,
                "duration": self.adjustment_interval if state == "on" else timedelta(0),
                "switch": switch,
            }
        )

        # Limit the history size to manage memory usage
        if len(self.history) > 1000:  # Adjust the size limit as needed
            self.history.pop(0)

    def turn_on_heat(self):
        for switch in self.heater_switch:
            self.set_heater_state(switch, "on")

    def turn_off_heat(self):
        for switch in self.heater_switch:
            self.set_heater_state(switch, "off")

    def duty_cycle_check(self, kwargs):
        """Check the current duty cycle and adjust switch states accordingly."""
        current_duty_cycle = calc_duty_cycle()

        # Compare and adjust each heater switch
        if current_duty_cycle > self.duty_cycle_percentage:
            self.turn_off_heat()
            self.log(
                f"Duty cycle exceeded: {current_duty_cycle:.2%}. Turning off heat."
            )
        else:
            self.turn_on_heat()
            self.log(
                f"Duty cycle below target: {current_duty_cycle:.2%}. Turning on heat."
            )
