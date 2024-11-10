#!/bin/bash

# Set the base directory for your add-on
BASE_DIR="duty-cycle-controller"

# Create the directory structure
mkdir -p $BASE_DIR/{apps,config}
cd $BASE_DIR

# Create config.json
cat <<EOL > config.json
{
  "name": "Duty Cycle Controller",
  "version": "1.0.0",
  "slug": "duty_cycle_controller",
  "description": "Manage underfloor heating using duty cycle logic.",
  "arch": ["armv7", "aarch64", "amd64", "i386"],
  "startup": "application",
  "boot": "auto",
  "ports": {
    "5050/tcp": 5050
  },
  "map": ["config", "ssl", "share", "addons"],
  "options": {
    "duty_cycle_percentage": 50,
    "min_pulse_width": 900,
    "history_duration": 3600,
    "adjustment_interval": 900
  },
  "schema": {
    "duty_cycle_percentage": "int",
    "min_pulse_width": "int",
    "history_duration": "int",
    "adjustment_interval": "int"
  },
  "image": "yourusername/duty-cycle-controller",
  "privileged": false
}
EOL

# Create Dockerfile
cat <<EOL > Dockerfile
# Use an official AppDaemon image as a base
FROM acockburn/appdaemon:latest

# Set up the working directory
WORKDIR /app

# Copy AppDaemon configuration and your app code
COPY apps/ /conf/apps/
COPY appdaemon.yaml /conf/appdaemon.yaml
COPY apps.yaml /conf/apps.yaml

# Run AppDaemon when the container starts
CMD ["appdaemon", "-c", "/conf"]
EOL

# Create run.sh (optional)
cat <<EOL > run.sh
#!/bin/bash
# Custom setup tasks if any
echo "Starting Duty Cycle Controller..."

# Start AppDaemon
exec appdaemon -c /conf
EOL

# Make run.sh executable
chmod +x run.sh

# Create README.md
cat <<EOL > README.md
# Duty Cycle Controller Add-on for Home Assistant

This add-on manages the duty cycle of an underfloor heating system using AppDaemon. It adjusts heating based on configurable duty cycles and adapts over time for energy efficiency.

## Installation

1. Clone this repository to your Home Assistant environment.
2. Copy the add-on folder into your Home Assistant configuration directory.
3. Navigate to **Supervisor > Add-on Store**, add the repository, and install the add-on.
4. Configure the add-on using the provided options.

## Configuration

The add-on supports the following configuration options:

- **duty_cycle_percentage**: The target duty cycle (0-100).
- **min_pulse_width**: Minimum on/off time in seconds.
- **history_duration**: The duration of time (in seconds) for which the duty cycle is measured retroactively.
- **adjustment_interval**: The time between each adjustment of the duty cycle in seconds.

## Usage

Start the add-on and monitor the logs to ensure it is running properly. Adjust the configuration in the Home Assistant UI as needed.
EOL

# Create .gitignore
cat <<EOL > .gitignore
# Ignore common files and directories
*.pyc
__pycache__/
.env
.vscode/
EOL

# Create a simple example AppDaemon app in apps directory
cat <<EOL > apps/duty_cycle_controller.py
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
EOL

echo "Add-on structure created successfully. Set up your Git origin and push the code."

