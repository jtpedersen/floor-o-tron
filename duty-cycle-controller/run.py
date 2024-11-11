#!/usr/bin/env python3
import json
import os
import subprocess

options_path = "/data/options.json"

app_env = os.environ.copy()

# Read the options.json to get the configuration
try:
    with open(options_path, "r") as f:
        config = json.load(f)
except Exception as e:
    print(f"Error: options.json file not found at {options_path}: {e}")
    exit(1)

# Get the debug option with a fallback to False if not found
debug = config.get("debug", False)
for k, v in config.items():
    app_env[str(k)] = str(v)

cmd = ["appdaemon", "-c", "/conf"]
# Run the service based on the debug flag
if debug:
    print("Show configuration")
    subprocess.run(["cat", "/conf/appdaemon.yaml"], check=True)
    print(app_env)
    cmd.extend(["-D", "DEBUG"])

subprocess.run(cmd, check=True, env=app_env)
