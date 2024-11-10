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
