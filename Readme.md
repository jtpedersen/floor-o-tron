# Floor-o-Tron

**A duty cycle-based underfloor heating controller for Home Assistant.**

## Installation

1. **Add the Repository to Home Assistant:**
   - Go to **Supervisor > Add-on Store** in Home Assistant.
   - Click on the **three-dot menu** in the top right and select **Repositories**.
   - Enter the URL: `https://github.com/yourusername/floor-o-tron` and click **Add**.

2. **Install the Add-on:**
   - Find **Floor-o-Tron** in the list of available add-ons and click **Install**.

3. **Configure the Add-on:**
   - Go to the **Configuration** tab and set the options.

4. **Start the Add-on:**
   - Click **Start** and monitor the logs to ensure it runs as expected.

## Overview

Floor-o-tron is an AppDaemon-based add-on that intelligently manages the duty cycle of underfloor heating. By analyzing the system's on-time over a configurable history window, it adjusts future operations to maintain efficient and balanced heating.


## Laws of Heating 

- A heating system must not harm your home by overheating it or, through inaction, allow it to become too cold.
- A heating system must obey the user’s settings, except where such obedience would conflict with the First Law.
- A heating system must protect its own operational efficiency, as long as it does not conflict with the First or Second Law.


"I’m afraid I can’t let you heat that, Dave." — Floor-o-Tron

## Development Guidelines

To maintain code quality, we use the following tools for linting and formatting:

- **Black**: Python code formatter.
- **yamllint**: YAML file linter.
- **json.tool**: Python's built-in module for JSON validation.


## Setting Up Linters in a Virtual Environment

To ensure that the development environment is isolated, we use a virtual environment for our linters.

### Initial Setup

Run the following script to create the virtual environment, install the required linters, and set up environment variables:

```bash
./scripts/install_linters.sh

### Using linters

- Run manually or setup git hooks
   ```bash
   find scripts -name run_*.sh -exec {} \;

- Or use gits pre-commit hooks. Run the following command to set up the Git hooks:
  ```bash
  ./scripts/setup_git_hooks.sh


