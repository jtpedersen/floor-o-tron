#!/usr/bin/env python3
import json
import os
import subprocess

# Path to the options.json file
options_path = "/data/options.json"

# Read the options.json to get the configuration
try:
    with open(options_path, "r") as f:
        config = json.load(f)
except Exception as e:
    print(f"Error: options.json file not found at {options_path}: {e}")
    exit(1)

# Get the debug option with a fallback to False if not found
debug = config.get("debug", False)

cmd = ["appdaemon", "-c", "/conf"]
# Run the service based on the debug flag
if debug:
    cmd.extend(["-D", "DEBUG"])

subprocess.run(cmd, check=True)
