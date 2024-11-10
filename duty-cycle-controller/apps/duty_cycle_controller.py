import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timedelta

class DutyCycleController(hass.Hass):
    def initialize(self):
        # Configuration parameters
        self.switch_entity = "switch.your_heating_switch"  # Replace with your actual switch entity ID
        self.duty_cycle_percentage = 0.5  # Initial duty cycle (50%)
        self.min_pulse_width = 15 * 60  # Minimum on/off time in seconds (default 15 minutes)
        self.history_duration = 3600  # History duration for measurement (default 1 hour)
        self.adjustment_interval = 900  # Time between duty cycle checks (e.g., 15 minutes)

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
