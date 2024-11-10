#!/bin/bash

# Export the token from the add-on options to the environment
export HA_TOKEN=$(bashio::config 'ha_token')
export HA_URL=$(bashio::config 'ha_url')

# Start AppDaemon with the correct configuration
exec appdaemon -c /conf
