import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timedelta
import utils


class DutyCycleController(hass.Hass):
    def initialize(self):

        heater_switch = self.args.get("heater_switch")
        if not isinstance(heater_switch, list):
            heater_switch = [heater_switch]
        self.duty_cycle_percentage = (
            float(self.args.get("duty_cycle_percentage")) / 100.0
        )
        self.min_pulse_width = utils.parse_time_literal(
            self.args.get("min_pulse_width", "15 minutes")
        )
        self.history_duration = utils.parse_time_literal(
            self.args.get("history_duration", "1 hour")
        )
        self.adjustment_interval = utils.parse_time_literal(
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
        end_time = datetime.now()
        start_time = end_time - self.history_duration
        for switch in self.heater_switch:
            history = self.get_history(
                entity_id=switch.entity_id, start_time=start_time
            )
            self.log(
                f"(History for {switch} since({start_time}) = {history}", level="DEBUG"
            )
            return utils.calculate_duty_cycle_from_history(
                history[0], self.history_duration, end_time
            )

    def duty_cycle_check(self, kwargs):
        """Check the current duty cycle and adjust switch states accordingly."""
        current_duty_cycle = self.calc_duty_cycle()

        # Compare and adjust each heater switch
        if current_duty_cycle > self.duty_cycle_percentage:
            self.log(
                f"Duty cycle exceeded: {current_duty_cycle:.2%} > < {self.duty_cycle_percentage}."
            )
            self.turn_off_heat()
        else:
            self.log(
                f"Duty cycle below target: {current_duty_cycle:.2%} < {self.duty_cycle_percentage}."
            )
            self.turn_on_heat()
