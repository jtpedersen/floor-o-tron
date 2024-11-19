import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
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

        self.log(f"Setting {switch} to {state}")

    def turn_on_heat(self):
        for switch in self.heater_switch:
            self.set_heater_state(switch, "on")

    def turn_off_heat(self):
        for switch in self.heater_switch:
            self.set_heater_state(switch, "off")

    def calc_duty_cycle(self):
        start_time = datetime.now() - self.history_duration
        for switch in self.heater_switch:
            history = self.get_history(
                entity_id=switch.entity_id, start_time=start_time
            )
            self.log(f"(History for {switch} = {history}")
            return utils.calculate_duty_cycle_from_history(
                history[0], end_time=datetime.now(tz=ZoneInfo("Europe/Copenhagen"))
            )

    def duty_cycle_check(self, kwargs):
        """Check the current duty cycle and adjust switch states accordingly."""
        current_duty_cycle = self.calc_duty_cycle()

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
