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
