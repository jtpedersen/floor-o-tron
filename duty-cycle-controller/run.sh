#!/bin/bash

# Load the debug option from the Home Assistant environment variables
DEBUG=$(jq --raw-output '.debug' /data/options.json)

if [ "$DEBUG" == "true" ]; then
  echo "Debug mode is enabled"
  # Start the add-on in debug mode, for example:
   appdaemon -c /conf -D DEBUG
else
  echo "Starting in normal mode"
   appdaemon -c /conf
fi
