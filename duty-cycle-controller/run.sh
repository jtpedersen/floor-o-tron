#!/bin/bash
# Custom setup tasks if any
echo "Starting Duty Cycle Controller..."

# Start AppDaemon
exec appdaemon -c /conf
