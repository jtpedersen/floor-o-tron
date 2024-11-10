import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timedelta
import re
from datetime import timedelta

def parse_time_literal(time_str):
    """Parses a time string like '1H', '1_hour', '15 minutes' into a timedelta object."""
    time_units = {
        's': 'seconds',
        'sec': 'seconds',
        'second': 'seconds',
        'seconds': 'seconds',
        'm': 'minutes',
        'min': 'minutes',
        'minute': 'minutes',
        'minutes': 'minutes',
        'h': 'hours',
        'hour': 'hours',
        'hours': 'hours',
        'd': 'days',
        'day': 'days',
        'days': 'days'
    }

    # Regex to match various time formats like '1H', '1_hour', '15 minutes'
    match = re.match(r'(\d+)\s*([a-zA-Z_]+)', time_str)
    if not match:
        raise ValueError(f"Invalid time format: {time_str}")

    value, unit = match.groups()
    unit = unit.lower().replace('_', '')

    if unit not in time_units:
        raise ValueError(f"Unsupported time unit: {unit}")

    # Create a timedelta object with the appropriate keyword argument
    return timedelta(**{time_units[unit]: int(value)})


class DutyCycleController(hass.Hass):
    def initialize(self):
        # Configuration parameters
        self.switch_entity = "switch.your_heating_switch"  # Replace with your actual switch entity ID
        self.duty_cycle_percentage = 0.5  
        self.min_pulse_width = parse_time_literal(self.args.get("min_pulse_width", "15 minutes"))
        self.duration = parse_time_literal(self.args.get("duration", "1 hour"))
        self.cycle_time = parse_time_literal(self.args.get("cycle_time", "1 day"))

        # Track on/off history
        self.history = []

        # Schedule the duty cycle check loop
        self.run_every(self.duty_cycle_check, "now", self.adjustment_interval)

    def duty_cycle_check(self, kwargs):
        now = datetime.now()

        # Clean history older than history_duration
        self.history = [entry for entry in self.history if entry['timestamp'] > now - timedelta(seconds=self.history_duration)]

        # Calculate total on-time and off-time
        on_time = sum(entry['duration'] for entry in self.history if entry['state'] == "on")
        total_time = self.history_duration

        # Calculate current duty cycle
        current_duty_cycle = on_time / total_time if total_time > 0 else 0

        # Compare and adjust
        if current_duty_cycle > self.duty_cycle_percentage:
            # Exceeds target duty cycle, turn off
            self.turn_off(self.switch_entity)
            self.log(f"Duty cycle exceeded: {current_duty_cycle:.2%}. Turning off.")
        else:
            # Below target duty cycle, turn on if not already on and pulse width permits
            if not self.get_state(self.switch_entity) == "on":
                self.turn_on(self.switch_entity)
                self.log(f"Duty cycle below target: {current_duty_cycle:.2%}. Turning on.")

        # Record the current action and timestamp for retroactive analysis
        state = self.get_state(self.switch_entity)
        self.history.append({
            'timestamp': now,
            'state': state,
            'duration': self.adjustment_interval if state == "on" else 0
        })
